use std::num::Wrapping;

// Constants from Wikipedia
const W: usize = 64;
const N: usize = 312;
const M: usize = 156;
const R: u64 = 31;
const F: Wrapping<u64> = Wrapping(6364136223846793005);

const A: Wrapping<u64> = Wrapping(0xB5026F5AA96619E9);
const U: usize = 29;
const D: Wrapping<u64> = Wrapping(0x5555555555555555);
const S: usize = 17;
const B: Wrapping<u64> = Wrapping(0x71D67FFFEDA60000);
const T: usize = 37;
const C: Wrapping<u64> = Wrapping(0xFFF7EEE000000000);
const L: usize = 43;
const MAGIC: [Wrapping<u64>; 2] = [Wrapping(0), A];

const DEFAULT_SEED: u64 = 5489;
const LOWER_MASK: Wrapping<u64> = Wrapping((1 << R) - 1);
const UPPER_MASK: Wrapping<u64> = Wrapping(!(LOWER_MASK.0));

// Intermediate constants
const MT_SIZE: usize = N as usize;

struct MersenneTwister64{
    mt: [Wrapping<u64>; MT_SIZE],
    index: usize,

}

impl MersenneTwister64 {
    fn new_unseeded() -> MersenneTwister64 {
        MersenneTwister64 {
            mt: [Wrapping(0);MT_SIZE],
            index: N+1,
        }
    }

    pub fn new() -> MersenneTwister64 {
        let mut mt = MersenneTwister64::new_unseeded();
        mt.seed_mt(DEFAULT_SEED);
        mt
    }

    pub fn new_from_array_seed(seed: &[u64]) -> MersenneTwister64 {
        let mut mt = MersenneTwister64::new_unseeded();
        mt.seed_by_array(seed);
        mt
    }

    pub fn seed_mt(&mut self, seed:u64) {
        self.index = N;
        self.mt[0] = Wrapping(seed);
        for i in 1..N {
            self.mt[i] = F * (self.mt[i-1] ^ (self.mt[i-1] >> (W-2))) + Wrapping(i as u64);
        }
    }

    pub fn seed_by_array(&mut self, seed:&[u64]) {
        let mut i = 1;
        let mut j = 0;
        let seed_len = seed.len();
        self.seed_mt(19650218);

        for _ in 0..N.max(seed_len) {
            self.mt[i] = (self.mt[i] ^ ((self.mt[i-1] ^ (self.mt[i-1] >> (W-2))) * Wrapping(3935559000370003845)))
                + Wrapping(seed[j]) + Wrapping(j as u64);
            i += 1;
            if i >= N {
                self.mt[0] = self.mt[N-1];
                i = 1;
            }
            j += 1;
            if j >= seed_len {
                j = 0;
            }
        }

        for _ in 0..N-1 {
            self.mt[i] = (self.mt[i] ^ ((self.mt[i-1] ^ (self.mt[i-1] >> (W-2))) * Wrapping(2862933555777941757)))
                - Wrapping(i as u64);
            i += 1;
            if i >= N {
                self.mt[0] = self.mt[N-1];
                i = 1;
            }
        }

        self.mt[0] = Wrapping(1 << (W-1) as u64);
    }

    pub fn next_u64(&mut self) -> u64{
        if self.index == N {
            self.twist();
        }

        let mut y = self.mt[self.index];
        y ^= (y >> U) & D;
        y ^= (y << S) & B;
        y ^= (y << T) & C;
        y ^= y >> L;

        self.index += 1;
        y.0
    }

    pub fn twist(&mut self) {
        for i in 0..(N-M) {
            let x = (self.mt[i] & UPPER_MASK) | (self.mt[i+1] & LOWER_MASK);
            self.mt[i] = self.mt[i+M] ^ (x >> 1) ^ MAGIC[(x.0 & 0x1) as usize];
        }

        for i in N-M..N-1 {
            let x = (self.mt[i] & UPPER_MASK) | (self.mt[i+1] & LOWER_MASK);
            self.mt[i] = self.mt[i - (N-M)] ^ (x >> 1) ^ MAGIC[(x.0 & 0x1) as usize];
        }

        let x = (self.mt[N-1] & UPPER_MASK) | (self.mt[0] & LOWER_MASK);
        self.mt[N-1] = self.mt[M-1] ^ (x >> 1) ^ MAGIC[(x.0 & 0x1) as usize];

        self.index = 0;
    }
}

#[test]
fn test_array_seed() {
    let mut mt = MersenneTwister64::new_from_array_seed(&[0x12345, 0x23456, 0x34567, 0x45678]);
    assert_eq!(mt.next_u64(), 7266447313870364031);
    assert_eq!(mt.next_u64(), 4946485549665804864);
}

#[test]
fn test_default_seed() {
    let mut mt = MersenneTwister64::new();
    assert_eq!(mt.next_u64(), 14514284786278117030);
}

