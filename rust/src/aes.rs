use crypto_pals::num_blocks;
use hex::decode;
use hex::encode;
use openssl::error::ErrorStack;
use openssl::symm::{decrypt, encrypt, Cipher};
use rand::Rng;
use std::io::Cursor;
use std::str::from_utf8;

const DEFAULT_KEY: &[u8] = b"YELLOW SUBMARINE";
const BYTE_SIZE: usize = 8;

pub struct MyCiphers {
    core: Cipher,
    key: Vec<u8>,
    block_size: usize,
}

impl MyCiphers {
    pub fn init_default() -> MyCiphers {
        MyCiphers {
            core: Cipher::aes_128_ecb(),
            block_size: DEFAULT_KEY.len() * BYTE_SIZE,
            key: DEFAULT_KEY.to_vec(),
        }
    }

    pub fn init(key: Vec<u8>) -> MyCiphers {
        MyCiphers {
            core: Cipher::aes_128_ecb(),
            block_size: key.len() * BYTE_SIZE,
            key
        }
    }

    pub fn getCore(&self) -> Cipher {
        self.core
    }

    pub fn getKey(&self) -> &Vec<u8> {
        &self.key
    }

    pub fn xcryptCtr(&self, text: &[u8], nonce: u64) -> Vec<u8> {
        let mut counter: u64 = 0;
        let keystream = self.generateKeystream(text, nonce);

        keystream
            .iter()
            .zip(text.iter())
            .map(|bytes: (&u8, &u8)| -> u8 { bytes.0 ^ bytes.1 })
            .collect()
    }

    pub fn generateKeystream(&self, text: &[u8], nonce: u64) -> Vec<u8> {
        let num_blocks = num_blocks(&self.key, text);
        let mut counter: u64 = 0;
        let mut keystream = vec![];

        for block_num in 0..num_blocks {
            let nonce_and_counter = [nonce.to_le_bytes(), counter.to_le_bytes()].concat();
            let mut stream_block = self.encryptEcb(nonce_and_counter.as_ref());
            keystream.append(&mut stream_block);
            counter += 1;
        }

        keystream.truncate(text.len());

        return keystream;
    }

    pub fn encryptEcb(&self, pt: &[u8]) -> Vec<u8> {
        // todo figure out Result handling
        encrypt(self.core, &self.key, None, &pt).unwrap()
    }

    pub fn decryptEcb(&self, ct: &[u8]) -> Vec<u8> {
        // todo figure out Result handling
        decrypt(self.core, &self.key, None, &ct).unwrap()
    }

    //s4c25 - CTR random access read/write
    pub fn edit(&self, ct: &mut [u8], nonce: u64, offset: usize, new_text: &[u8]) -> Vec<u8> {
        let keystream = self.generateKeystream(ct, nonce);
        let end_offset = offset + new_text.len();
        let keystream_subset = &keystream[offset..end_offset];

        let mut new_ct: Vec<u8> = new_text.to_vec()
            .iter()
            .zip(keystream_subset.iter())
            .map(|bytes: (&u8, &u8)| -> u8 { bytes.0 ^ bytes.1 })
            .collect();

        for i in 0..new_text.len() {
            ct[i+offset] = new_ct[i];
        }

        return ct.to_vec();
    }
}

#[test]
fn test_encrypt_decrypt_ecb() {
    let cipher = MyCiphers::init_default();

    let pt = b"this is 32 charsthis is 32 chars";
    let ct = cipher.encryptEcb(pt);
    let result = cipher.decryptEcb(&ct);

    assert_eq!(pt, &result[..]);
}

#[test]
fn test_encrypt_decrypt_ctr() {
    let cipher = MyCiphers::init_default();
    let mut rng = rand::thread_rng();
    let nonce: u64 = rng.next_u64();

    // 128 bytes
    let pt = b"this is 32 charsthis is 32 chars";

    let ct = cipher.xcryptCtr(pt, nonce);
    let result = cipher.xcryptCtr(&ct, nonce);

    assert_eq!(pt, &result[..]);
}
