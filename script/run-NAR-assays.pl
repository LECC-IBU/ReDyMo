#!/usr/bin/perl -w

# This file is part of ReDyMo.
#
#    Copyright (c) 2018  Gustavo Cayres and Marcelo Reis.
#
#    ReDyMo is free software: you can redistribute it and/or modify it
#    under the terms of the GNU General Public License as published by the
#    Free Software Foundation, either version 3 of the License, or (at your
#    option) any later version.
#    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#    for more details.
#    You should have received a copy of the GNU General Public License along
#    with ReDyMo. If not, see <http://www.gnu.org/licenses/>.
#
#

# Computational assays in da Silva et al. (2018), manuscript submitted
# for publication in Nucleic Acids Research (NAR).

use strict;

# The simulations were carried out with a very big timeout (== 100000000!),
# in order to allow full replication.
#
my $TIMEOUT = 100000000;

# Number of simulations per set of parameters (i.e., each simulation is
# considered to be the S-phase of an independent cell).
#
my $NUMBER_OF_CELLS = 2; 

# Output path.
#
my $PATH = "../output/";

# Clean up output directory before the experiments.
#
system ("rm -rf $PATH");
system ("mkdir $PATH");

for (my $F = 10; $F <= 20; $F += 10)
#for (my $F = 10; $F <= 100; $F += 10)
{
  foreach my $period (0, 900)
#  foreach my $period (0, 900, 750, 600, 450, 300, 150, 90)
  {
    foreach my $has_dormant ('False', 'True')
    {
      ($has_dormant eq 'False')
        and printf "Running assay with F = $F, period = $period and " . 
                   "no dormant origin firing (%d cells)... ",
                   $NUMBER_OF_CELLS 
         or printf "Running assay with F = $F, period = $period and " . 
                   "with dormant origin firing (%d cells)... ",
                   $NUMBER_OF_CELLS;  
    
      system("time python3 ../src/main.py " .
             "--organism 'Trypanosoma brucei brucei TREU927' " .
             "--dormant $has_dormant " . 
             "--resources $F " .
             "--speed 1 " . 
             "--period $period " .
             "--timeout $TIMEOUT " .
             "--cells $NUMBER_OF_CELLS " .
             "1> " . $PATH . $has_dormant . "_" . $F . "_" . $period . "_out ".
             "2> " . $PATH . $has_dormant . "_" . $F . "_" . $period . "_err");

      print "[done]\n";
    }
  }
}

# End of program.
#
exit 0;

