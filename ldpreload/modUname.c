#include <stdio.h>
#include <string.h>
#include <sys/utsname.h>
#include "modUname.h"

int uname(struct utsname *u){
	strcpy(u->sysname,"Linux");
	strcpy(u->nodename,"");
	strcpy(u->release,RELEASE);
	strcpy(u->version,"");
	strcpy(u->machine,"x86_64");
	return 0;
};
