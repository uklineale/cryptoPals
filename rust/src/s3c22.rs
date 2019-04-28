extern crate rand;
extern crate chrono;

mod mersenne_twister;

use self::mersenne_twister::MersenneTwister64;
use chrono::{DateTime, Duration, Utc};
use rand::Rng;

fn main() {
    let mut rng = rand::thread_rng();

    let t1 = rng.gen_range(40,1000);
    let t2 = rng.gen_range(40,1000);

    let seed = (Utc::now() + Duration::seconds(t1)).timestamp() as u64;
    let mut mt = MersenneTwister64::new(seed);

    println!("Seeding MT with {}", seed);

    let out = mt.next_u64();
    println!("Got {}", out);


    let start_crack = (Utc::now() + Duration::seconds(t1+t2)).timestamp() as u64;
    println!("Starting search at {}", start_crack);

    let answer = crack_mt_timestamp(out, start_crack);
    if let Some(x) = answer {
        let mut clone_mt = MersenneTwister64::new(x);
        clone_mt.next_u64();

        for _ in 0..1000 {
            assert_eq!(mt.next_u64(), clone_mt.next_u64());
        }
    } else {
        println!("FAIL");
    }

}

fn crack_mt_timestamp(output: u64, start: u64) -> Option<u64> {
    let iterations = 1000*2;

    for i in 0..iterations {
        let guess = start - i;
        let mut guess_mt = MersenneTwister64::new(guess);
        if guess_mt.next_u64() == output {
            println!("Found seed of {}", guess);
            return Some(guess);
        }
    }
    None
}