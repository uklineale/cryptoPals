extern crate rand;
mod mersenne_twister;

use self::mersenne_twister::MersenneTwister64;
use rand::Rng;

fn main() {
    let mut rng = rand::thread_rng();
    let seed = rng.next_u64();
    let mut mt = MersenneTwister64::new(seed);

    const STATE_LEN : usize =  312;
    let mut outputs: [u64; STATE_LEN] = [0; STATE_LEN];
    let mut state: [u64; STATE_LEN] = [0; STATE_LEN];

    for i in 0..STATE_LEN {
        outputs[i] = mt.next_u64();
    }

    for i in 0..STATE_LEN {
        state[i] = MersenneTwister64::untemper(outputs[i]);
    }

    // Check state matches
    let actual_state = mt.dump_state();
    for i in 0..STATE_LEN {
        assert_eq!(state[i], actual_state[i].0);
    }

    let mut cloned = MersenneTwister64::clone_from_state(&state);

    // Check cloned MT predicts original
    for _ in 0..1000 {
        assert_eq!(mt.next_u64(), cloned.next_u64());
    }

    // Aw. Yeah.
}