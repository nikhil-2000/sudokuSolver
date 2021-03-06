#include <iostream>
#include <vector>
#include <tuple>
#include <string>
#include <fstream>
#include "sudokuSolver.h"

class Grid {
  public:
    int grid[9][9];
    std::vector< std::tuple<int,int> > gaps;

    void main(std :: string oneLineSudoku) {
      //Input file name

      fillGrid(oneLineSudoku);
      fillGaps();
      outputGrid();
      std :: cout << "Solving ...";
      solveGrid();

      std :: cout << "\n\n";
      outputGrid();

    }

    std::string getOneLineGrid() {
      char currentChar;
      std::string oneLineGrid = "";
      for (int i = 0;  i < 9; i++){
        for (int j = 0;  j < 9; j++ ){
          currentChar = grid[i][j];
          oneLineGrid = oneLineGrid+currentChar;
        }
    
      }

      return oneLineGrid;
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
   
    void fillGrid(std::string oneLineSudoku){
      

      int i = 0;
      int x,y;

      for (char& n : oneLineSudoku){
        x = (i) / 9;
        y = (i) % 9;
        grid[x][y] = n - '0';
        i++;
      }

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

    bool rowOkay(int i,int j){
      int cellVal = grid[i][j];
      for (int c = 0; c < 9 ; c++){
        if (grid[i][c] == cellVal && c != j){
          return false;
        }
      }
      return true;
    }

    bool colOkay(int i,int j){
      int cellVal = grid[i][j];
      for (int r = 0; r < 9 ; r++){
        if (grid[r][j] == cellVal && r != i){
          return false;
        }
      }
      return true;
    }

    bool boxOkay(int i, int j){
      int cellVal = grid[i][j];
      int r,c;
      int startR, startC;
      startR = i - (i % 3);
      startC = j - (j % 3);
      for (r = startR; r < startR + 3; r++){
        for (c = startC; c < startC + 3; c ++){
          if (grid[r][c] == cellVal && (r != i || c != j)){
            return false;
          }
        }
      }
      return true;
    }

    void outputBox(int i , int j){
      int cellVal = grid[i][j];
      int r,c;
      int startR, startC;
      startR = i - (i % 3);
      startC = j - (j % 3);
      for (r = startR; r < startR + 3; r++){
        for (c = startC; c < startC + 3; c ++){
          std :: cout << grid[r][c];
          
        }
        std :: cout << "\n";

      }
    }

    bool valueFits(int i, int j){
      return rowOkay(i,j) && colOkay(i,j) && boxOkay(i,j);
    }

    int getTupleRow(std::tuple<int,int> t){
      return std::get<0>(t);
    }

    int getTupleCol(std::tuple<int,int> t){
      return std::get<1>(t);
    }

    bool solveGap(int i, int j){

      // std :: cout << i << " " << j << "\n";
      
      grid[i][j] ++;
      
      while (!(valueFits(i,j))){
        grid[i][j] ++;
      }

      if (grid[i][j] > 9) {
        grid[i][j] = 0;
        return false;
      }else{
        return true;
      }

    }

    void solveGrid(){
      int row,col;
      bool gapSolved;
      int count = 0;
      
      int currentGap = 0;
      
      while (currentGap < gaps.size()){
        row = getTupleRow(gaps.at(currentGap)); 
        col = getTupleCol(gaps.at(currentGap));
        
        gapSolved = solveGap(row,col);
//        count ++;
//        if (count == 1000000){
//          std :: cout << "\n\n\n\n";
//          outputGrid();
//          count = 0;
//        }
      


        if (gapSolved){
          currentGap ++;
        }else{
          currentGap --;
        }

        if (currentGap < 0){
          std :: cout << "Unsolvable Grid\n";
        }
        // call solve gap on current space
        // if true
          //move on to next gap
        // if false
          //call solve gap on previous gap        
      }

    }

};

std::string solveSudoku(std :: string oneLineSudoku) {
    Grid sudokuGrid;
    sudokuGrid.main(oneLineSudoku);
    return sudokuGrid.getOneLineGrid();
}


int main(int argc, char *argv[]) {
  std::string oneLineSudoku = argv[1];
  solveSudoku(oneLineSudoku);
  return 0;
}

void outputOne(){
  std::cout << "1";
}