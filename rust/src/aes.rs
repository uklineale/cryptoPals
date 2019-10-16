use crypto_pals::num_blocks;
use hex::decode;
use hex::encode;
use openssl::error::ErrorStack;
use openssl::symm::{decrypt, encrypt, Cipher};
use rand::Rng;
use std::io::Cursor;
use std::str::from_utf8;

pub struct MyCiphers {
    core: Cipher,
    key: String,
    block_size: usize,
}

impl MyCiphers {
    pub fn init() -> MyCiphers {
        let key = "YELLOW SUBMARINE".to_string();
        MyCiphers {
            core: Cipher::aes_128_ecb(),
            block_size: key.len(),
            key,
        }
    }

    pub fn getCore(&self) -> Cipher {
        self.core
    }

    pub fn getKey(&self) -> &String {
        &self.key
    }

    pub fn xcryptCtr(&self, text: &[u8], nonce: u64) -> Vec<u8> {
        let mut counter: u64 = 0;
        let mut result: Vec<u8> = vec![];
        let num_blocks = num_blocks(self.key.as_bytes(), text);

        for block_num in 0..num_blocks {
            // Is every bit equally likely (statistically)?
            let keystream = self.generateKeystream(nonce, counter, self.key.as_bytes().to_vec());
            counter += 1;
            let block_start = block_num * self.block_size;
            let block = &text[block_start..block_start + self.block_size];

            let mut crypted: Vec<u8> = keystream
                .iter()
                .zip(block.iter())
                .map(|bytes: (&u8, &u8)| -> u8 { bytes.0 ^ bytes.1 })
                .collect();

            result.append(&mut crypted);
        }
        println!("len of result: {}", result.len());

        return result;
    }

    pub fn generateKeystream(&self, nonce: u64, ctr: u64, key: Vec<u8>) -> Vec<u8> {
        let nonce_and_counter = [nonce.to_le_bytes(), ctr.to_le_bytes()].concat();
        self.encryptEcb(nonce_and_counter.as_ref())
    }

    pub fn encryptEcb(&self, pt: &[u8]) -> Vec<u8> {
        // todo figure out Result handling
        encrypt(self.core, self.key.as_bytes(), None, &pt).unwrap()
    }

    pub fn decryptEcb(self, ct: &[u8]) -> Vec<u8> {
        // todo figure out Result handling
        decrypt(self.core, self.key.as_bytes(), None, &ct).unwrap()
    }
}

#[test]
fn test_encrypt_decrypt_ecb() {
    let cipher = MyCiphers::init();

    let pt = b"this is 32 charsthis is 32 chars";
    let ct = cipher.encryptEcb(pt);
    let result = cipher.decryptEcb(&ct);

    assert_eq!(pt, &result[..]);
}

#[test]
fn test_encrypt_decrypt_ctr() {
    let cipher = MyCiphers::init();
    let mut rng = rand::thread_rng();
    let nonce: u64 = rng.next_u64();

    // 128 bytes
    let pt = b"this is 32 charsthis is 32 chars";

    let ct = cipher.xcryptCtr(pt, nonce);
    let result = cipher.xcryptCtr(&ct, nonce);

    assert_eq!(pt, &result[..]);
}
