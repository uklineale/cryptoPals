#[crate_id = "commons"]
#[crate_type = "lib"]

extern crate hex;
extern crate base64;

pub fn hex_to_base64(s: &str) -> String {
    let bytes = hex::decode(s).unwrap();
    base64::encode(&bytes)
}

pub fn base64_to_hex(s: &str) -> String {
    let bytes = base64::decode(s).unwrap();
    hex::encode(&bytes)
}

pub fn xor_hex(hex1: &str, hex2: &str) -> String {
    if hex1.len() != hex2.len() { }
    let bytes =
}



#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    fn test_hex_to_base64() {
        let hex_str = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
        let expected_b64 = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t";

        assert_eq!(hex_to_base64(hex_str), expected_b64)
    }

    #[test]
    fn test_base64_to_hex() {
        let b64_str = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t";
        let expected_hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";

        assert_eq!(base64_to_hex(b64_str), expected_hex)
    }

    fn test_xor() {

    }
}
