#!/usr/bin/env node
'use strict';

const ecc = require('@hiveio/hive-js/lib/auth/ecc');

const seed = process.argv[2];
const messageB64 = process.argv[3];

if (!seed || !messageB64) {
  console.error('usage: node hive_js_sign_buffer_oracle.js <seed> <message-base64>');
  process.exit(2);
}

const message = Buffer.from(messageB64, 'base64').toString('utf8');
const privateKey = ecc.PrivateKey.fromSeed(seed);
const publicKey = privateKey.toPublicKey().toString('STM');
const signature = ecc.Signature.signBuffer(message, privateKey);
const signatureHex = signature.toHex();
const recovered = ecc.Signature.fromHex(signatureHex)
  .recoverPublicKeyFromBuffer(message)
  .toString('STM');

if (recovered !== publicKey) {
  throw new Error('Hive-JS oracle failed self-recovery');
}

process.stdout.write(JSON.stringify({
  seed,
  message_utf8_hex: Buffer.from(message, 'utf8').toString('hex'),
  public_key: publicKey,
  signature_hex: signatureHex,
  recovered_public_key: recovered,
}) + '\n');
