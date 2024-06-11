//Library initialization
#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <mpi.h>
#include <time.h>
#include <cblas.h>

// Define the sparsity of the matrix M
#define SPARSITY 0.6

// Create a random sparse matrix by column
void randomMatriceM(int a, int b, double *A){

  //Define the same initialisation to have the same matrix in every algorithms
  srand(1);
  
  for (int i = 0; i < a ; i++) {
    for (int j = 0; j < b ; j++) {
      // Check if a random value between 0 and 1 is less than the sparsity factor
      if ((double)rand() / RAND_MAX < SPARSITY) {
        
        // Take a random number between 0 to 9
        A[a*j + i] = rand() % 10;  
      }
    }
  }
}

// Create a random matrix by column
void randomMatricev(int a, int b, double *A){

  //Define the same initialisation to have the same matrix in every algorithms
  srand(1);

  for (int i = 0; i < a ; i++) {
    for (int j = 0; j < b ; j++) {
    
      // Take a random number between 0 to 9 ...
      A[a*j + i] = rand() % 10; 
      
      // ... but change if it is 0
      if (A[a*j + i] == 0) {
   	    A[a*j + i] = rand() % 10 + 1;
      } 
    }
  }
}

// Function to determine the number of row to send each process and the resulting parameters
void determine_rownumbers(int m,int n,int k, int npes, int *colnumbers,int *sendcountsN, int *displsN,int *sendcountsM, int *displsM) { 

  // if m is not a multiplier of process numbers
  if ((k%npes) != 0) {
  
    // Define the number of row for each process
    for (int i=0; i<npes; i++) {
    
      // Process balancing 
      if (i< (k%npes)) {
      
        colnumbers[i] = ((k - (k%npes))/npes) + 1;  
    
    } else {
      colnumbers[i] = ((k - (k%npes))/npes) ;
    }
  }
  
  } else {
  
    for (int i=0; i<npes; i++) {
    
      colnumbers[i] = (k/npes);
    
    }
  
  }
  
  // Define the size of the rows to be sent to each process 
  for(int u=0; u<npes; u++) {
  
    sendcountsN[u] = colnumbers[u] * n;
  }
  
  // Define the location in the matrix of items to be sent to each process 
  for(int j=1; j<npes; j++) {
  
    displsN[j] = displsN[j-1] + colnumbers[j-1]*n;
  }
  
  
  // Define the size of the rows to be received by 0 for each process
  for(int u=0; u<npes; u++) {
  
    sendcountsM[u] = colnumbers[u] * m ;
  }
  
  // Define the location in the matrix of items to be received by 0 for each process
  for(int j=1; j<npes; j++) {
  
    displsM[j] = displsM[j-1] + colnumbers[j-1] * m;
  }

}


// Main function of algorithm 1 
int main(int argc, char *argv[]) {
  
  //Initalisation csv
  FILE *file;
  
  // MPI initialization
  int myrank, npes;
  MPI_Status status; 
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &npes);
  MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
  
  //Time initalization 
  double start, end;
  start = MPI_Wtime();
  
  // Initialization of matrices parameters
  int m = atoi(argv[1]); 
  int n = atoi(argv[2]);
  int k = atoi(argv[3]);
  
  double *M = (double *)calloc(m * n, sizeof(double));
  double *v = (double *)calloc(n * k, sizeof(double)); 
  double *Mat = (double *)calloc(m * k, sizeof(double));
  
  // Initialization of communications parameters
  int *colnumbers = (int *)calloc(npes, sizeof(int));
  int *sendcountsN = (int *)calloc(npes, sizeof(int));
  int *displsN = (int *)calloc(npes, sizeof(int));
  int *sendcountsM = (int *)calloc(npes, sizeof(int));
  int *displsM = (int *)calloc(npes, sizeof(int));
  
  determine_rownumbers(m,n,k, npes, colnumbers,sendcountsN, displsN, sendcountsM, displsM);
  
  int c = colnumbers[myrank];
  
  // Initialization of matricies for communications
  double *vsmall= (double *)calloc(n * c, sizeof(double));
  double *smallMat = (double *)calloc(m * c, sizeof(double));
  
  if(myrank == 0) {
   
    printf("\nAlgorithm2_cblas m:%d n:%d k:%d\n\n",m,n,k);
    
    // Creation of random matricies
  	randomMatriceM(m,n,M);
  	randomMatricev(n,k,v);
    
	}
  
  // Broadcast matrix v to all process
  MPI_Bcast(M, m*n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
  
  // Send rows to processes
	MPI_Scatterv(v,sendcountsN,displsN, MPI_DOUBLE, vsmall, n*c,MPI_DOUBLE, 0,MPI_COMM_WORLD);
  
  // Matricies multiplication calculation
  cblas_dgemm(CblasColMajor, CblasNoTrans, CblasNoTrans, m, c, n, 1.0, M, m, vsmall, n, 0.0, smallMat, m);
  
  // Group the final rows in a matrix
	MPI_Gatherv(smallMat, m*c,MPI_DOUBLE, Mat, sendcountsM, displsM,MPI_DOUBLE,0,MPI_COMM_WORLD);
  
  end = MPI_Wtime();
 
  if (myrank == 0) {
  
    double total_time = end - start;
   
    printf("Total time : %fs\n", total_time ); 
    
    //Write data into csv  
    file = fopen("time.csv","a");
   
    fprintf(file,"\n%d,%d,%d,%s,%f,%d", m,n,k, "algorithm2_cblas", total_time, npes);
    
    fclose(file);
  }
 
  MPI_Finalize();
  
  // Free the memory
  free(M);
  free(v);
  free(Mat);
  free(vsmall);
  free(smallMat);
  
  return 0;
  
}
  
  
  
  
  
  
