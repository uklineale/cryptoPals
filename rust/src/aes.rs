use openssl::symm::{encrypt, Cipher, decrypt};
use rand::Rng;
use openssl::error::ErrorStack;

const UPPER_64_BITS: u128 = 0x11111111111111110000000000000000;
const LOWER_64_BITS: u128 = 0x00000000000000001111111111111111;


pub struct MyCiphers {
    core: Cipher,
    key: String,
}

impl MyCiphers {
    pub fn init() -> MyCiphers {
        MyCiphers {
            core: Cipher::aes_128_ecb(),
            key: "YELLOW SUBMARINE".to_string(),
        }
    }

    pub fn getCore(&self) -> Cipher {
        self.core
    }

    pub fn getKey(&self) -> &String {
        &self.key
    }

    pub fn encryptCtr(&self, pt: String) -> String {
        let mut rng = rand::thread_rng();

        // Theoretically all bits are equally random?
        let nonce: u128 = rng.next_u64() as u128;
        let mut counter: u128 = 0x0;

        let mut num_blocks = pt.len() / self.key.len();
        if pt.len() % self.key.len() > 0 {
            num_blocks += 1;
        }

        for block in 0..num_blocks {
            let key_stream = (nonce & UPPER_64_BITS) & (counter & LOWER_64_BITS);
            counter += 1;
            self.encryptEcb(&key_stream.to_be_bytes());
        }

        "dud".to_string()
    }


    pub fn encryptEcb(&self, pt: &[u8]) -> Result<Vec<u8>, ErrorStack> {
        encrypt(self.core, self.key.as_bytes(), None,  &pt)
    }

    pub fn decryptEcb(self, ct: &[u8]) -> Result<Vec<u8>, ErrorStack> {
        decrypt(self.core, self.key.as_bytes(), None, &ct)
    }

}

#[test]
fn test_encrypt_ecb() {
    let cipher = MyCiphers::init();
}
