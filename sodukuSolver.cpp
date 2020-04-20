#include <iostream>
#include <vector>
#include <tuple>
#include <string>
#include <fstream>

class Grid {
  public:
    int grid[9][9];
    std::vector< std::tuple<int,int> > gaps;

    void main() {
      //Input file name
      fillGrid("unsolved soduku.txt");
      fillGaps();

    }

    void outputGrid(){
      bool bottomLine = false;
    
      for (int i = 0;  i < 9; i++){

        if (i % 3 == 2){
          bottomLine = true;
        }

        for (int j = 0;  j < 9; j++ ){

          std::cout << grid[i][j];

          if (j % 3 == 2 && j != 8) {
            std::cout << "|";
          }

        }
        
        std::cout << '\n';

        if (bottomLine && i != 8){

          for (int j = 0;  j < 11; j++ ){

            if (j % 4 == 3) {
              std::cout << "+";
            }else{
              std::cout << "-";
            }
          }

          std::cout << '\n';
          bottomLine = false;

        }
      }
    }

    void outputGaps(){
      for (std::vector<int>::size_type i = 0; i < gaps.size(); i++) {
	      outputTuple(gaps.at(i));
      }
    }

  private:
    void fillGrid(std::string filename){
      std::ifstream inFile;
      std::string oneLineSoduku;
      std::string num;
      
      inFile.open(filename);

      while (inFile >> num){
        oneLineSoduku.append(num);
      }

      int i = 0;
      int x,y;
      for (char& n : oneLineSoduku){
        x = (i) / 9;
        y = (i) % 9;
        grid[x][y] = n - '0';
        i++;
      }


      inFile.close();
    }

    bool isGap(int i,int j) {
      return (grid[i][j] == 0);
    }

    void outputTuple(std::tuple <int , int> t){

      std::cout << std::get<0>(t) << std::get<1>(t) << ' ' << '\n'; 

    }
    
    void fillGaps(){
      std::tuple<int,int> loc;

      for (int i = 0;  i < 9; i++){

        for (int j = 0;  j < 9; j++ ){

          if (isGap(i,j)){

            loc = {i,j};
            gaps.insert(gaps.end(),loc);
          }
        }
      }
    }

};


int main() {
  Grid sodukuGrid;
  sodukuGrid.main();
  sodukuGrid.outputGrid();
  return 0;
}