//Library initialization
#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <mpi.h>
#include <time.h>

// Define the sparsity of the matrix M
#define SPARSITY 0.6

// Create a random sparse matrix by column
void randomMatriceM(int a, int b, int *A){

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

// Create a random matrix by row
void randomMatricev(int a, int b, int *A){

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

//Rearrange M by line 
int* rearrange(int a,int b, int *A) {
  
  int *AR = (int *)calloc(a * b, sizeof(int));
  
  for (int i =0; i<a; i++) {
    for (int j=0; j<b; j++) {
    
      AR[b*i + j] = A[a*j + i];
    }
  
  }
  
  return AR;

}


// Multiplication of two matricies
void MatrixMultiplication(int m, int n, int k, int *M,int *v, int *Mat) {
 
  // Browse rows, columns and the shared dimension
  for(int i=0; i<m; i++) {
    for(int j=0; j<k; j++) {
      int newpoint=0;
      for(int u=0; u<n;u++) {
        newpoint += M[n * i + u] * v[j + u * k];
      }
    Mat[i*k + j] = newpoint; 
    }
  }
}

// Function to determine the number of row to send each process and the resulting parameters
void determine_rownumbers(int m,int n,int k, int npes, int *Nnumbers,int *sendcountsM, int *displsM,int *sendcountsK, int *displsK) { 

  // if m is not a multiplier of process numbers
  if ((n%npes) != 0) {
  
    // Define the number of row for each process
    for (int i=0; i<npes; i++) {
    
      // Process balancing 
      if (i< (n%npes)) {
      
        Nnumbers[i] = ((n - (n%npes))/npes) + 1;  
    
    } else {
      Nnumbers[i] = ((n - (n%npes))/npes) ;
    }
  }
  
  } else {
  
    for (int i=0; i<npes; i++) {
    
      Nnumbers[i] = (n/npes);
    
    }
  
  }
  
  // Define the size of the rows to be sent to each process 
  for(int u=0; u<npes; u++) {
  
    sendcountsM[u] = Nnumbers[u] * m;
  }
  
  // Define the location in the matrix of items to be sent to each process 
  for(int j=1; j<npes; j++) {
  
    displsM[j] = displsM[j-1] + Nnumbers[j-1]*m;
  }
  
  
  // Define the size of the rows to be received by 0 for each process
  for(int u=0; u<npes; u++) {
  
    sendcountsK[u] = Nnumbers[u] * k ;
  }
  
  // Define the location in the matrix of items to be received by 0 for each process
  for(int j=1; j<npes; j++) {
  
    displsK[j] = displsK[j-1] + Nnumbers[j-1]*k;
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
  
  int *M = (int *)calloc(m * n, sizeof(int));
  int *v = (int *)calloc(n * k, sizeof(int)); 
  int *Mat = (int *)calloc(m * k, sizeof(int));
  
  // Initialization of communications parameters
  int *Nnumbers = (int *)calloc(npes, sizeof(int));
  int *sendcountsM = (int *)calloc(npes, sizeof(int));
  int *displsM = (int *)calloc(npes, sizeof(int));
  int *sendcountsK = (int *)calloc(npes, sizeof(int));
  int *displsK = (int *)calloc(npes, sizeof(int));
  
  determine_rownumbers(m,n,k, npes, Nnumbers,sendcountsM, displsM, sendcountsK, displsK);
  
  int N = Nnumbers[myrank];
  
  // Initialization of matricies for communications
  int *Msmall= (int *)calloc(m * N, sizeof(int));
  int *vsmall= (int *)calloc(N * k, sizeof(int));
  int *smallMat = (int *)calloc(m * k, sizeof(int));
  
  if(myrank == 0) {
   
    printf("\nAlgorithm3 m:%d n:%d k:%d\n\n",m,n,k);
    
    // Creation of random matricies
  	randomMatriceM(m,n,M);
  	randomMatricev(n,k,v);
	}
  
  // Send columns and rows to processes
	MPI_Scatterv(M,sendcountsM,displsM, MPI_INT, Msmall, m*N,MPI_INT, 0,MPI_COMM_WORLD);
  MPI_Scatterv(v,sendcountsK,displsK, MPI_INT, vsmall, N*k,MPI_INT, 0,MPI_COMM_WORLD);
  
  Msmall = rearrange(m,N,Msmall);
  
  // Matricies multiplication calculation
  MatrixMultiplication( m, N, k, Msmall, vsmall, smallMat);
  
	// Group and sum the matricies to obtain a final matrix
  MPI_Reduce(smallMat, Mat, m*k, MPI_INT, MPI_SUM, 0,MPI_COMM_WORLD);
  
  end = MPI_Wtime();
 
  if (myrank == 0) {
  
    double total_time = end - start;
   
    printf("Total time : %fs\n", total_time ); 
    
    //Write data into csv  
    file = fopen("time.csv","a");
   
    fprintf(file,"\n%d,%d,%d,%s,%f,%d", m,n,k, "algorithm3", total_time, npes);
    
    fclose(file);
    
  }
 
  MPI_Finalize();
  
  // Free the memory
  free(M);
  free(v);
  free(Mat);
  free(Msmall);
  free(vsmall);
  free(smallMat);
  
  return 0;
  
}
  
  
  
  
  
  