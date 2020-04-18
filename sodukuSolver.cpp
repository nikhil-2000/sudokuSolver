#include <iostream>
using namespace std;

class Grid {
  public:
    int grid[9][9];

    void fillGrid(){
      for (int i = 0;  i < 9; i++){
        for (int j = 0;  j < 9; j++ ){
          grid[i][j] = 0;
        }
      }
    }

    void outputGrid(){
      bool bottomLine = false;
      for (int i = 0;  i < 9; i++){
        if (i % 3 == 2){
          bottomLine = true;
        }
        for (int j = 0;  j < 9; j++ ){
          cout << grid[i][j];
          if (j % 3 == 2 && j != 8) {
            cout << "|";
          }
        }
        
        cout << '\n';
        if (bottomLine && i != 8){
          for (int j = 0;  j < 11; j++ ){
            if (j % 4 == 3) {
              cout << "+";
            }else{
              cout << "-";
            }
          }
          cout << '\n';
          bottomLine = false;
        }
      }
    }
};


int main() {
  Grid sodukuGrid;
  sodukuGrid.fillGrid();
  sodukuGrid.outputGrid();
  return 0;
}