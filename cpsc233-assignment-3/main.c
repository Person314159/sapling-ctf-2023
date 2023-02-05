#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>

typedef void student_func();

int read_shellcode(char * dest, int length) {
    char * hex_str = malloc(length*2+1);
    ssize_t n_bytes = read(0,hex_str,length*2);
    for (ssize_t i=0;i<n_bytes/2;i++){
        if (!sscanf(&hex_str[i*2],"%2hhx",&dest[i])) {
            return 0;
        };
    }
    free(hex_str);
    return 1;
}

int assignment_3(void * func, int full_mark) {
    ((student_func *)func)();
    printf("Code sumbitted\n");
    return full_mark;
}

void init_chall() {
    alarm(60);
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
}

int main() {
    init_chall();
    srand(time(NULL));
    char * func = mmap((void *)0x2333000,0x1000,7,0x21,0,0);
    puts("please put your function shellcode here: ");
    if (!read_shellcode(func,0x10)) {
        puts("fail to read shellcode, please check your shellcode");
        exit(-1);
    };
    int total = 0x10;
    int grade = assignment_3((void *) func, total);
    printf("Your Grade: %d/%d\n",grade,total);
}