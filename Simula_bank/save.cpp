#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
int Tiempo_servicio = [3, 5, 5, 1, 4, 1, 5, 5, 6, 1, 3, 6, 1, 3, 5, 2, 4, 4, 1, 5, 4, 1, 3, 3, 5, 5, 3, 1, 3, 3, 4, 2, 3, 5, 6, 1, 5, 2, 2, 2, 2, 6, 4, 2, 4, 3, 5, 3, 2, 4];
  string data = "";
  ofstream file;
  file.open("ServiceTime.csv");
   for (int i=0;i<50;i++)
   {
    data += to_string(Tiempo_servicio[i])+"\n";
    cout << data;
   }
  file << data;
  file.close();
  return 0;
}
