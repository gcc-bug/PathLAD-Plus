#ifndef MAIN_H
#define MAIN_H

#include <stdbool.h> 
int run_solver(int timeLimit,            // default value: 60
               bool firstSol,          // default value: false
               int number_Sol,             // default value: 1 or whatever is appropriate
               bool induced,           // default value: false
               int verbose,                // default value: 0
               const char* fileNameGp,
               const char* fileNameGt);

#endif
