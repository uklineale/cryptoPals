mod aes;

use aes::MyCiphers;
use hex::{encode, decode};
use rand::{Rng, RngCore};
use std::fs;
use std::str::from_utf8;
use std::borrow::BorrowMut;

// This is inefficient. You can set the plaintext to the ciphertext,
// then CTR will decrypt it for you!
pub fn crack_random_access_ctr(cipher: &MyCiphers, ct: &mut [u8], nonce: u64) -> Vec<u8> {
    let mut cracked: Vec<u8> = vec!();

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

pub fn main() {
    let mut rng = rand::thread_rng();
    let nonce: u64 = rng.next_u64();

    let mut key_bytes: [u8;16] = [0; 16];
    rng.fill_bytes(&mut key_bytes);
    let key = key_bytes.to_vec();

    let c = MyCiphers::init(key);

    let pt = b"This is a secret. Have I successfully decrypted this?";

    let mut ct = c.xcryptCtr(pt, nonce);
    let ct_clone = ct.clone();
    let result = c.edit(&mut ct, nonce, 0,  &ct_clone);
    println!("{}", from_utf8(&result).unwrap());
}
