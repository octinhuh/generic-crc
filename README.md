# Generic CRC Generator
## Summary
This repository includes Python scripts that allow for the quick creation and
use of generic cyclic reduncancy check implementations, as well as 
a supporting generic binary linear feedback shift register (LFSR) and polynomial
divider.
## Use Case
This code's reliance on generic polynomial division, rather than the bit-wise
operations of non-flexible CRC implementations means it is not very high
performance, but it allows for flexibility in switching CRC generators for
prototyping or simulation purposes.
## Instructions
In your python project,

```import CRC```

And create a CRC unit with the integer representation of the generator
polynomial and length (in bytes) of the payload. For example, the generator for
the 32-bit ANSI CRC is ```0x18005```. This example is demonstrated in `main` of
`CRC.py`.