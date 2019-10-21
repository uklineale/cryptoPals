extern crate rand;
extern crate byteorder;
extern crate hex;
pub mod mersenne_twister;

use rand::Rng;
use rand::RngCore;
use rand::distributions::Alphanumeric;
use mersenne_twister::MersenneTwister64;
use std::iter;
use std::vec::Vec;
use std::string::String;

const SEED_MASK: u64 = 0x000000000000FFFF;
const LOWEST_BYTE_MASK: u64 = 0x00000000000000FF;

fn encrypt(key: u64, pt: &String) -> String {
    let key_stream = generate_keystream(key, pt);
    let bytes = pt.as_bytes();
    let mut enc_bytes = vec!();
    for i in 0..bytes.len() {
        enc_bytes.push(bytes[i] ^ key_stream[i]);
    }
    return hex::encode(enc_bytes);
}

fn decrypt(key: u64, ct: &String) -> String {
    let key_stream = generate_keystream(key, ct);
    let bytes = hex::decode(ct).unwrap();
    let mut dec_bytes: Vec<u8> = vec!();
    for i in 0..bytes.len() {
        dec_bytes.push(bytes[i] ^ key_stream[i]);
    }
    let ptResult = String::from_utf8(dec_bytes);
    match ptResult {
        Ok(pt) => {
            return pt;
        }, Err(e) => {
            // invalid ct
            return "".to_string();
        },
    }
}

fn generate_keystream(key: u64, text: &String) -> Vec<u8> {
    let len = text.len() / 8 + 1;
    let mut mt = MersenneTwister64::new(key & SEED_MASK);
    let doubles: Vec<u64> = iter::repeat(mt.next_u64())
        .take(len)
        .collect();

    let mut keystream : Vec<u8> = vec!();
    for item in doubles {
        for i in 0..8 {
            keystream.push(((item >> (8 * i)) & LOWEST_BYTE_MASK) as u8);
        }
    }

    return keystream;
}

fn crack_seed(ct: &String, known_pt: &str) -> u64 {
    for i in 0..2u64.pow(16) {
        let pt = decrypt(i, ct);
        if pt.contains(known_pt) {
            return i;
        }
    }
    return 0;
}

fn main() {
    let mut rng = rand::thread_rng();
    let seed = rng.next_u64();

    let num_rand_chars = rng.gen_range(1, 50);
    let chars: String = iter::repeat(())
        .map(|()| rng.sample(Alphanumeric))
        .take(num_rand_chars)
        .collect();

    let known_pt = "AAAAAAAAAAAAAA";
    let rand_text = chars + known_pt;

    let ct = encrypt(seed, &rand_text);
    let pt = decrypt(seed, &ct);

    assert!(rand_text == pt);

    let broken_seed = crack_seed(&ct, known_pt);

    println!("Expected seed is {} \n Actual seed is {}", seed & SEED_MASK, broken_seed);
}