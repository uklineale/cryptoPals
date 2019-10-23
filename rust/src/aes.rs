use crypto_pals::num_blocks;
use openssl::symm::{decrypt, encrypt, Cipher};
use rand::{Rng,RngCore};

const DEFAULT_KEY: &[u8] = b"YELLOW SUBMARINE";

pub struct MyCiphers {
    core: Cipher,
    key: Vec<u8>,
}

impl MyCiphers {
    pub fn init_default() -> MyCiphers {
        MyCiphers {
            core: Cipher::aes_128_ecb(),
            key: DEFAULT_KEY.to_vec(),
        }
    }

    pub fn init(key: Vec<u8>) -> MyCiphers {
        MyCiphers {
            core: Cipher::aes_128_ecb(),
            key
        }
    }

    pub fn get_core(&self) -> Cipher {
        self.core
    }

    pub fn get_key(&self) -> &Vec<u8> {
        &self.key
    }

    pub fn xcrypt_ctr(&self, text: &[u8], nonce: u64) -> Vec<u8> {
        let _counter: u64 = 0;
        let keystream = self.generate_keystream(text, nonce);

        keystream
            .iter()
            .zip(text.iter())
            .map(|(x,y)| x ^ y)
            .collect()
    }

    pub fn generate_keystream(&self, text: &[u8], nonce: u64) -> Vec<u8> {
        let num_blocks = num_blocks(&self.key, text);
        let mut counter: u64 = 0;
        let mut keystream = vec![];

        for _block_num in 0..num_blocks {
            let nonce_and_counter = [nonce.to_le_bytes(), counter.to_le_bytes()].concat();
            let mut stream_block = self.encrypt_ecb(nonce_and_counter.as_ref());
            keystream.append(&mut stream_block);
            counter += 1;
        }

        keystream.truncate(text.len());

        return keystream;
    }

    pub fn encrypt_ecb(&self, pt: &[u8]) -> Vec<u8> {
        // todo figure out Result handling
        encrypt(self.core, &self.key, None, &pt).unwrap()
    }

    pub fn decrypt_ecb(&self, ct: &[u8]) -> Vec<u8> {
        // todo figure out Result handling
        decrypt(self.core, &self.key, None, &ct).unwrap()
    }

    //s4c25 - CTR random access read/write
    pub fn edit(&self, ct: &mut [u8], nonce: u64, offset: usize, new_text: &[u8]) -> Vec<u8> {
        let keystream = self.generate_keystream(ct, nonce);
        let end_offset = offset + new_text.len();
        let keystream_subset = &keystream[offset..end_offset];

        new_text.iter()
            .zip(keystream_subset)
            .map(|(x,y)|x ^ y)
            .enumerate()
            .for_each(|(i, val)| ct[i+offset]=val);

        return ct.to_vec();
    }
}

#[test]
fn test_encrypt_decrypt_ecb() {
    let cipher = MyCiphers::init_default();

    let pt = b"this is 32 charsthis is 32 chars";
    let ct = cipher.encrypt_ecb(pt);
    let result = cipher.decrypt_ecb(&ct);

    assert_eq!(pt, &result[..]);
}

#[test]
fn test_encrypt_decrypt_ctr() {
    let cipher = MyCiphers::init_default();
    let mut rng = rand::thread_rng();
    let nonce: u64 = rng.next_u64();

    // 128 bytes
    let pt = b"this is 32 charsthis is 32 chars";

    let ct = cipher.xcrypt_ctr(pt, nonce);
    let result = cipher.xcrypt_ctr(&ct, nonce);

    assert_eq!(pt, &result[..]);
}
