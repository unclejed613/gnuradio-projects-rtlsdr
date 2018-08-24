this is a simple "voice inversion" scrambler.  this scrambling system was popular in the 1960s and 1970s for scrambling 
telephone calls. WARNING: this is the "CAESAR CIPHER" of audio scramblers. it can easily be identified, and anybody
with simple electronics or signal processing skills can decode it. children's toys such as the "Darth Vader Voice Changer"
contain the hardware needed to decode the output of this scrambler with some minor modification. this is far from a truly secure
method of scrambling speech.

the way this scrambler functions is the input audio is sent through a balanced mudulator (multiplier), with a "carrier" input 
provided by a 3khz oscillator.  the output of the modulator is a double sideband supressed carrier signal (sum and difference
frequencies of the input audio and carrier). the signal is sent through a low pass filter with a cutoff of 2700hz to remove the
upper sideband portion of the signal, leaving the lower sideband only.  this lower sideband signal is an "inverted" copy of
the original audio, with low frequencies swapping places with high frequencies.  to decode the scrambled signal, the audio
is passed through the scrambler again (in a telephone or radio setup, it would be another scrambler), and the audio output is a
"re-inverted" copy of the original audio.  that property makes this a symmetrical system, the same process that scrambles the
signal also unscrambles it.  the use of this scrambler on a SSB radio can easily be defeated by switching a receiver to the 
opposite sideband and tuning 3khz high or low (depending on which mode the transmitter is using).

this flowgraph is not meant to be used for secure communications, because the method is so well known and easily
broken.  it is, however an interesting piece of technology, and was used in the past for a reasonably secure method
of scrambling audio (as long as it wasn't used over an SSB radio).  the advent of monolithic 4-quadrant multiplier ICs made 
decoding scrambled audio simple and easy, and this scrambler was rapidly made obsolete.


when testing this flowgraph, remember to change to file paths to something sane (they are currently set to /home/user/)
and substitute a wav file with speech in it for the original source audio (currently set to scramtest2b.wav, which is not 
included with the flowgraph and python script).  make sure to enable and disable the proper wav file sources and sinks
when testing the flowgraph (hopefully the filenames are descriptive enough).
