import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { TransactionStatus } from "genlayer-js/types";
import { privateKeyToAccount } from "viem/accounts";
import { createInterface } from "node:readline/promises";

const contract = process.env.CONTRACT_ADDRESS;
if (!/^0x[0-9a-fA-F]{40}$/.test(contract || "")) throw new Error("Set CONTRACT_ADDRESS");
if (process.stdin.isTTY && process.stdin.setRawMode) process.stdin.setRawMode(true);
const input = createInterface({ input: process.stdin, terminal: false });
const credentials = JSON.parse(await input.question("")); input.close();
if (process.stdin.isTTY && process.stdin.setRawMode) process.stdin.setRawMode(false);
const keys = [credentials.walletA, credentials.walletB];
if (keys.some((key) => !/^(0x)?[0-9a-fA-F]{64}$/.test(key || ""))) throw new Error("Provide two keys through stdin");
const wallets = keys.map((key) => privateKeyToAccount(key.startsWith("0x") ? key : `0x${key}`));
const reader = createClient({ chain: studionet });
const writer = (wallet) => createClient({ chain: studionet, account: wallet });
const read = (functionName, args = []) => reader.readContract({ address: contract, functionName, args });
const parse = async (functionName, args = []) => JSON.parse(await read(functionName, args));
const transactions = [];
const write = async (wallet, functionName, args, label) => {
  const hash = await writer(wallet).writeContract({ address: contract, functionName, args });
  console.log(JSON.stringify({ event: "submitted", label, hash }));
  let receipt;
  for (let attempt = 0; attempt < 40; attempt++) {
    try { receipt = await reader.waitForTransactionReceipt({ hash, status: TransactionStatus.FINALIZED }); break; }
    catch (error) { if (attempt === 39) throw error; await new Promise((resolve) => setTimeout(resolve, 5000)); }
  }
  const detail = await reader.getTransaction({ hash });
  const tx = { actor: wallet.address, hash, label, resultName: detail.result_name || detail.resultName || "UNKNOWN", status: receipt.status_name || receipt.status };
  transactions.push(tx); console.log(JSON.stringify({ event: "finalized", ...tx }));
};
const guard = async (action, label) => {
  const before = await parse("get_counts"); await action(); const after = await parse("get_counts");
  if (JSON.stringify(before) !== JSON.stringify(after)) throw new Error(`${label} mutated counters`);
};

const owner = "Azaria723", repo = "WebhookSchemaDriftCourt", commit = "43e30aa751bfe422162288ed52a775232435a7a4";
const source = (path, digest) => JSON.stringify({ owner, repo, commit, path, digest });
const scenarios = [
  { name:"removed-field", event:"payment.completed", pointer:"/data/customer/id", allegation:"Removing the stable customer identifier may break the billing consumer at the registered pointer.", expected:"BREAKING_CHANGE", digests:["13c55dbd5369af183ff8d974d86063d18ac506cdaa280246f65473e648332dbe","e2d42a85aa352d11e9a2ac45d6ab77cd8aad1aeb635968e11d79072f1d2cb5a7","0352192f2e4070b369709843a2bb1c7a9407ba3d21c93e8d85a816fe5349ac28"] },
  { name:"additive-optional", event:"payment.completed", pointer:"/data/customer_id", allegation:"Adding an optional receipt property should preserve the documented consumer dependency and compatibility.", expected:"COMPATIBLE", digests:["64b48c73ca809442849b6f79919c604314cbe07cebb85bb8757f206174062adc","5be72904d151069a8ae165c5d9cb41d4ffea2cc157ef9f20f94edec730129203","7bd407b88ca86a7cc2c35fc93c9e2ef03a66d76e120d206b8f55a5c88c769c97"] },
  { name:"ambiguous-migration", event:"account.changed", pointer:"/data/owner_id", allegation:"Moving the owner identifier requires the documented dual-read migration before removing the original pointer.", expected:"MIGRATION_REQUIRED", digests:["9e92b507eb9c22493ee52c3831383c26c8d732c1758798c89eef8383fe9fdd2b","fe57129ca453fe7c62b63cea43637db95befc88651c5bda847d1e237f5662f8c","1f29dce2d9e460431f86608b433eabe11d6c65a46aadf4dc2b3c0f12503cc789"] },
  { name:"removed-field", event:"payment.completed", pointer:"/data/customer/id", allegation:"An intentionally incorrect before-schema digest must fail closed before compatibility judgment.", expected:"SOURCE_UNVERIFIED", digests:["0".repeat(64),"e2d42a85aa352d11e9a2ac45d6ab77cd8aad1aeb635968e11d79072f1d2cb5a7","0352192f2e4070b369709843a2bb1c7a9407ba3d21c93e8d85a816fe5349ac28"] }
];
const slots = ["BEFORE_SCHEMA", "AFTER_SCHEMA", "CONSUMER_CONTRACT"];
const files = ["before.json", "after.json", "consumer.md"];

let counts = await parse("get_counts");
for (let id = counts.case_count; id < scenarios.length; id++) {
  const item = scenarios[id];
  await write(wallets[id % 2], "register_case", [item.event, item.pointer, item.allegation], `register_${id}_${item.name}`);
}
for (let id = 0; id < scenarios.length; id++) {
  const item = scenarios[id];
  for (let index = 0; index < slots.length; index++) {
    const existing = await parse("get_snapshot", [BigInt(id), slots[index]]);
    if (existing.error) await write(wallets[(id + index) % 2], "bind_snapshot", [BigInt(id), slots[index], source(`/fixtures/${item.name}/${files[index]}`, item.digests[index])], `bind_${id}_${slots[index].toLowerCase()}`);
  }
  let state = await parse("get_case", [BigInt(id)]);
  if (state.state === "REGISTERED") await write(wallets[(id + 1) % 2], "seal_case", [BigInt(id)], `seal_${id}`);
}
await guard(() => write(wallets[0], "bind_snapshot", [0n, "BEFORE_SCHEMA", source("/fixtures/removed-field/before.json", scenarios[0].digests[0])], "post_seal_mutation_guard"), "post-seal mutation");
await guard(() => write(wallets[1], "seal_case", [999n], "missing_case_guard"), "missing case");
await guard(() => write(wallets[0], "register_case", ["x", "bad", "This deliberately malformed case must not alter any state counter in the live contract."], "invalid_case_guard"), "invalid case");
for (let id = 0; id < scenarios.length; id++) {
  const state = await parse("get_case", [BigInt(id)]);
  if (state.state === "ASSESSABLE") await write(wallets[(id + 1) % 2], "assess_case", [BigInt(id)], `assess_${id}_${scenarios[id].name}`);
}
const cases = await Promise.all(scenarios.map((_, id) => parse("get_case", [BigInt(id)])));
for (let id = 0; id < scenarios.length; id++) if (cases[id].verdict !== scenarios[id].expected) throw new Error(`case ${id} expected ${scenarios[id].expected}: ${JSON.stringify(cases[id])}`);
await guard(() => write(wallets[1], "assess_case", [0n], "terminal_replay_guard"), "terminal replay");
counts = await parse("get_counts");
console.log(JSON.stringify({ chainId: studionet.id, contract, wallets: wallets.map((w) => w.address), counts, cases, transactions }, null, 2));
