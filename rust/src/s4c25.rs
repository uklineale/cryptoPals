mod aes;

use aes::MyCiphers;

pub fn main() {
    let cipher = MyCiphers::init();
    let strang = &cipher.encryptEcb("abc".as_bytes()).unwrap();
    let destrang = &cipher.decryptEcb(&strang).unwrap();





    println!("We can do it too Cyborgs! {:?}\n {:?}", destrang, b"abc");
}