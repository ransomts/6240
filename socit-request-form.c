#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

int ask_yn_question(char * question) {
  
  char answer[3]; // memory is cheap, spring for the extra two bytes
  printf("%s (yN) ", question);
  scanf("%s", &answer);
  
  // for ( ; *answer; ++answer) *answer = tolower(*answer);
  for(int i = 0; answer[i]; i++){
    answer[i] = tolower(answer[i]);
  }
  
  return strcmp(answer, "yes") || strcmp(answer, "y");
}

int get_install_justification(char * justification) {
  printf("Succinctly, why should this package be installed?\n");
  printf("(Hitting enter sends the email, C-c to quit, you have one tweet of space (280 chars))\n\n");
  scanf("%s", justification);
}

int send_request_email(char * justification) {
  // the user gets 280 characters, the command needs 60
  char mail_command[340] = "mail -s 'request for program install' socit@clemson.edu <<< '"; 
  
  // strcpy(mail_command, "mail -s 'request for program install' socit@clemson.edu <<< ");
  strcat(mail_command, justification);
  strcat(mail_command, "'");
  // printf("%s\n", mail_command);
  int status = system(mail_command);
  printf("email, has been sent :)\n");
  return status;
}

int main(){
  int response;
  response = ask_yn_question("Would you like to submit a request to SoCIT to install this package?");
  //printf("%d\n", response);
  // if (response != 0) exit(0);

  response = ask_yn_question("Before we begin, have you considered installing this package local to your home directory?");
  //printf("%d\n", response);
  /// if (response != 0) exit(0);

  char justification[280]; // the length of one tweet
  get_install_justification(justification);

  return send_request_email(justification);
}
