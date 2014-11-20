#!/usr/bin/python

import symex.z3str
import z3

## Construct two 32-bit integer values.  Do not change this code.
a = z3.BitVec('a', 32)
b = z3.BitVec('b', 32)

## Compute the average of a and b.  The initial computation we provided
## naively adds them and divides by two, but that is not correct.  Modify
## these lines to implement your solution for both unsigned (u_avg) and
## signed (s_avg) division.
##
## Watch out for the difference between signed and unsigned integer
## operations.  For example, the Z3 expression (x/2) performs signed
## division, meaning it treats the 32-bit value as a signed integer.
## Similarly, (x>>16) shifts x by 16 bits to the right, treating it
## as a signed integer.
##
## Use z3.UDiv(x, y) for unsigned division of x by y.
## Use z3.LShR(x, y) for unsigned (logical) right shift of x by y bits.

a_lo = z3.Extract(15, 0, a)
b_lo = z3.Extract(15, 0, b)
a_lo = z3.ZeroExt(1, a_lo)
b_lo = z3.ZeroExt(1, b_lo)
#a_lo and b_lo are now both 17 bits long
#16 for math, one for rollover bit

a_hi = z3.Extract(31, 16, a)
b_hi = z3.Extract(31, 16, b)
a_hi = z3.ZeroExt(1, a_hi)
b_hi = z3.ZeroExt(1, b_hi)
#a_hi and b_hi are now 17 bits, the top 16 bits of them
#plus one for rollover

lo = a_lo + b_lo
#Top bit is whether or not to have the upper bits added to
hi_add_bit = z3.Extract(16, 16, lo)
#sign extend so can add to the existing values, is same length
hi_add_bit = z3.ZeroExt(16, hi_add_bit)
hi = a_hi + b_hi
hi = hi + hi_add_bit

#Now have the correct added top 16 bits plus rollover, 
#and the bottom bits plus their rollover

#Hey, division by two is a right shift!
#So take all the bottom 16 bits but the bottom,
#this is our lower set of bits
total = z3.Extract(15, 1, lo)
#zero extend to 32 so have a place to put the new incoming bits
total = z3.ZeroExt(17, total)

hi = z3.LShR(-16, hi)
hi = z3.ZeroExt(15, hi)

u_avg = total + hi
s_avg = u_avg

## Do not change the code below.

## To compute the reference answers, we extend both a and b by one
## more bit (to 33 bits), add them, divide by two, and shrink back
## down to 32 bits.  You are not allowed to "cheat" in this way in
## your answer.
az33 = z3.ZeroExt(1, a)
bz33 = z3.ZeroExt(1, b)
real_u_avg = z3.Extract(31, 0, z3.UDiv(az33 + bz33, 2))

as33 = z3.SignExt(1, a)
bs33 = z3.SignExt(1, b)
real_s_avg = z3.Extract(31, 0, (as33 + bs33) / 2)

def do_check(msg, e):
    print "Checking", msg, "using Z3 expression:"
    print "    " + str(e).replace("\n", "\n    ")
    solver = z3.Solver()
    solver.add(e)
    ok = solver.check()
    print "  Answer for %s: %s" % (msg, ok)

    if ok == z3.sat:
        m = solver.model()
        print "  Example solution:", m

do_check("unsigned avg", u_avg != real_u_avg)
do_check("signed avg", s_avg != real_s_avg)
