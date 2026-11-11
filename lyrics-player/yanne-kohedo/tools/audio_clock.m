#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#include <unistd.h>

// Report the actual playback position; Python never estimates MP3 time from size.
int main(int argc, const char **argv) {
  @autoreleasepool {
    if (argc < 2 || argc > 3) return 2;
    NSError *error = nil;
    NSURL *url = [NSURL fileURLWithPath:[NSString stringWithUTF8String:argv[1]]];
    AVAudioPlayer *player = [[AVAudioPlayer alloc] initWithContentsOfURL:url error:&error];
    if (!player || ![player prepareToPlay]) {
      fprintf(stderr, "%s\n", [[error description] UTF8String]); return 1;
    }
    printf("DURATION %.6f\n", player.duration); fflush(stdout);
    if (argc == 3) player.currentTime = MAX(0, MIN(player.duration, strtod(argv[2], NULL)));
    if (![player play]) return 1;
    while (player.playing) {
      printf("TIME %.6f\n", player.currentTime); fflush(stdout);
      usleep(10000);
    }
    printf("END %.6f\n", player.duration); fflush(stdout);
  }
  return 0;
}
