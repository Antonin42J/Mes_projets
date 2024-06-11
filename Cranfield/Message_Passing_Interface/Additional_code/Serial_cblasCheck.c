//Library initialization
#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <mpi.h>
#include <time.h>
#include <cblas.h>

// Define the sparsity of the matrix M
#define SPARSITY 0.6

// Create a random sparse matrix by row
void randomMatriceM(int a, int b, double *A){

  //Define the same initialisation to have the same matrix in every algorithms
  srand(1);
  
  for (int i = 0; i < a ; i++) {
    for (int j = 0; j < b ; j++) {
      // Check if a random value between 0 and 1 is less than the sparsity factor
      if ((double)rand() / RAND_MAX < SPARSITY) {
        
        // Take a random number between 0 to 9
        A[b*i + j] = rand() % 10;  
      }
    }
  }
}

// Create a random matrix by row
void randomMatricev(int a, int b, double *A){

  //Define the same initialisation to have the same matrix in every algorithms
  srand(1);

  for (int i = 0; i < a ; i++) {
    for (int j = 0; j < b ; j++) {
    
      // Take a random number between 0 to 9 ...
      A[b*i + j] = rand() % 10; 
      
      // ... but change if it is 0
      if (A[b*i + j] == 0) {
   	    A[b*i + j] = rand() % 10 + 1;
      } 
    }
  }
}



// Main function of algorithm 1 
int main(int argc, char *argv[]) {
  
  // MPI initialization
  int myrank,npes;
  MPI_Status status; 
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &npes);
  MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
  
  // Initialization of matrices parameters
  int m = atoi(argv[1]); 
  int n = atoi(argv[2]);
  int k = atoi(argv[3]);
  
  double *M = (double *)calloc(m * n, sizeof(double));
  double *v = (double *)calloc(n * k, sizeof(double)); 
  double *Mat = (double *)calloc(m * k, sizeof(double));
  
  if(myrank == 0) {
   
    printf("\nSerial_cblas m:%d n:%d k:%d\n\n",m,n,k);
    
    // Creation of random matricies
  	randomMatriceM(m,n,M);
  	randomMatricev(n,k,v);
    
    // Matricies multiplication calculation
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, m, k, n, 1.0, M, n, v, k, 0.0, Mat, k);
    
    printf("Mat:\n");
    for (int i = 0; i < m; ++i) {
      for (int j = 0; j < k; ++j) {
        printf("%f\t", Mat[j + k * i]);
      }
      printf("\n");
    }
    
    printf("\n\n\n");
  }
 
  MPI_Finalize();
  
  // Free the memory
  free(M);
  free(v);
  free(Mat);
  
  return 0;
  
}
  
  
  
  
  
  