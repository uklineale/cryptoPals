mod aes;

use aes::MyCiphers;
use hex::encode;
use rand::Rng;

pub fn main() {
    let cipher = MyCiphers::init();

    let mut rng = rand::thread_rng();
    let nonce: u64 = rng.next_u64();

    // 128 bytes
    let pt = b"this is 32 charsthis is 32 chars";

    let ct = cipher.xcryptCtr(pt, nonce);
    let result = cipher.xcryptCtr(&ct, nonce);

    print!("expected: {:?}\nresult:   {:?}", encode(pt), encode(result));
}
