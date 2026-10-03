import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
import { privateKeyToAccount } from 'viem/accounts';
import { createInterface } from 'node:readline/promises';

const address = process.env.CONTRACT_ADDRESS;
if (!/^0x[0-9a-fA-F]{40}$/.test(address || '')) throw new Error('Set CONTRACT_ADDRESS');
if (process.stdin.isTTY && process.stdin.setRawMode) process.stdin.setRawMode(true);
const input = createInterface({ input: process.stdin, terminal: false });
const { walletB } = JSON.parse(await input.question('')); input.close();
if (process.stdin.isTTY && process.stdin.setRawMode) process.stdin.setRawMode(false);
if (!/^(0x)?[0-9a-fA-F]{64}$/.test(walletB || '')) throw new Error('Invalid wallet input');
const account = privateKeyToAccount(walletB.startsWith('0x') ? walletB : `0x${walletB}`);
const reader = createClient({ chain: studionet });
const writer = createClient({ chain: studionet, account });
const parse = async (fn, args = []) => JSON.parse(await reader.readContract({ address, functionName: fn, args }));
const before = await parse('get_counts');
const beforeCase = await parse('get_case', [5n]);
const raw = await writer.writeContract({ address, functionName: 'assess_case', args: [5n] });
const hash = typeof raw === 'string' ? raw : raw.txId;
let detail;
for (let attempt = 0; attempt < 90; attempt++) {
  detail = await reader.getTransaction({ hash });
  const status = detail.statusName || detail.status_name || detail.status;
  if (status === 'FINALIZED' || status === 7) break;
  await new Promise(resolve => setTimeout(resolve, 5000));
}
const after = await parse('get_counts');
const afterCase = await parse('get_case', [5n]);
if (JSON.stringify(before) !== JSON.stringify(after) || JSON.stringify(beforeCase) !== JSON.stringify(afterCase)) throw new Error('terminal replay mutated canonical state');
console.log(JSON.stringify({ actor: account.address, hash, status: detail.statusName || detail.status_name || detail.status, execution: detail.result_name || detail.resultName, before, after, case5: afterCase }, null, 2));
