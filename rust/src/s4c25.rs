mod aes;

use aes::MyCiphers;

use rand::{RngCore};
use std::fs;
use std::string::String;


// This is inefficient. You can set the plaintext to the ciphertext,
// then CTR will decrypt it for you!
pub fn crack_random_access_ctr(cipher: &MyCiphers, ct: &mut [u8], nonce: u64) -> Vec<u8> {
    let mut cracked = vec!();

    for i in 0..ct.len() {
        let target = ct[i].clone();
        for guess in 0..255u8 {
            cipher.edit(ct, nonce, i, &[guess]);
            if target == ct[i] {
                cracked.extend_from_slice(&[guess]);
                break;
            }
        }
    }

    return cracked;
}

pub fn get_ct(cipher: &MyCiphers, nonce: u64) -> Vec<u8> {
    let default_cipher = MyCiphers::init_default();

    let encoded_ct = fs::read_to_string("src/files/s4c25").expect("Can't read file.");
    let trimmed: String = encoded_ct.chars()
        .filter(|c| *c != '\n')
        .collect();
    let decoded_ct = base64::decode(&trimmed).expect("Can't decode file");

    let pt = default_cipher.decrypt_ecb(&decoded_ct);
    cipher.xcrypt_ctr(&pt, nonce)
}


pub fn main() {
    let mut rng = rand::thread_rng();
    let nonce: u64 = rng.next_u64();

    let mut key_bytes: [u8;16] = [0; 16];
    rng.fill_bytes(&mut key_bytes);
    let key = key_bytes.to_vec();

    let c = MyCiphers::init(key);

    let mut ct = get_ct(&c, nonce);
    let ct_clone = ct.clone();

    let result = c.edit(&mut ct, nonce, 0,  &ct_clone);
    println!("{}", String::from_utf8_lossy(&result));
}
