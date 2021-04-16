#include <stdio.h> 
#include <time.h>
#include <stdlib.h>
#define upper 8
#define lower 0
#define N 9

int matrix[9][9];
int a[9][9];

//check if the value is safe to put in the particular column and row
int isSafe(int *x, int row, int col, int num)
{
    int grid[9][9];
	for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			grid[i][j] = x[j%9+i*9];
		}
	}

	for (int k = 0; k <= 8; k++)
		if (grid[row][k] == num)
			return 0;

	for (int k = 0; k <= 8; k++)
		if (grid[k][col] == num)
			return 0;
        
	int startRow = row - row % 3;
	int startCol = col - col % 3;
       
	for (int i = 0; i < 3; i++)
		for (int j = 0; j < 3; j++)
			if (grid[i + startRow][j + startCol] == num)
				return 0;

	return 1;
}


//generating array of random numbers 
int *generator()
{
    int temp,random,random2;
    
    int *arr = (int*)malloc(sizeof(int)*9);
    for(int i=0;i<9;i++)
        arr[i] = i+1;
    
    srand ( time(NULL) );
    for(int i=0;i<9;i++)
    {
        random = (rand() % (upper - lower + 1)) + lower ;
        random2 = (rand() % (upper - lower + 1)) + lower ;
        temp = arr[random];
        arr[random] = arr[random2];
        arr[random2] = temp;    
    }
    return arr;
}

//rotating the generated array 
int  *leftRotatebyOne(int *x, int n)
{
    int *a;
    a = x;
    int temp = a[0], i;
    for (i = 0; i < n - 1; i++)
        a[i] = a[i + 1];
    a[n-1] = temp;
    return a;
}


//calling the above function 3 times
int *rotator(int *y,int*x,int n)
{
    y = leftRotatebyOne(x,n);
    y = leftRotatebyOne(y,n);
    y = leftRotatebyOne(y,n);
    return y;
}

//calling the above function 1 time
int *rotator_single(int *y,int*x,int n)
{
    y = leftRotatebyOne(x,n);
    return y;
}

//generating final question
int final_quest(int d)
{
    int x;
    if(d==1)
    {
        x = 25;
    }
    else if(d ==2)
    {
        x = 55;
    }
    else if(d == 3)
    {
        x = 75;
    }
    srand ( time(NULL) );
    for(int i=0;i<x;i++)
    {
        int random = (rand() % (upper - lower + 1)) + lower ;
        int random2 = (rand() % (upper - lower + 1)) + lower ;
        if(matrix[random][random2] !=0)
        {
            matrix[random][random2] =0;
        }
    }
}


//convert two d array to one d for simplictiy in calculation
void *twod_to_oned()
{
    int *array;
    array = (int*)malloc(sizeof(int)*81);
    for(int i=0;i<9;i++)
    {
        for(int j=0;j<9;j++)
        {
            array[i * 9 + j] = matrix[i][j] ;
        }
    }


    return array;
  
}


//remove some values from the generated question to make it sudoku
int *get_question(int d)
{
    int *x,*y,*q;
    int n = 9;
    int j=0;
    x = generator();
    y = rotator(y,x,n);
    for(int k=0;k<9;k++)
    {
        if(k>0 && k<3)
        {
            y = rotator(y,y,n);
        }
        else if(k == 3 || k == 6)
        {
            y= rotator_single(y,x,n);
        }
        else
        {
            y = rotator(y,y,n);
        }
        for(int l=0;l<9;l++)
        {
            matrix[k][l] = y[l];
        }
    }
    final_quest(d);
    q = twod_to_oned();
    return q;
}


//get the answer from backtracking
int  solveSuduko(int row, int col)
{
	int *passer = (int*)malloc(sizeof(int)*81);

    for(int i=0;i<9;i++)
    {
        for(int j=0;j<9;j++)
        {
            passer[i * 9 + j] = a[i][j] ;
        }
    }


    if (row == N - 1 && col == N)
		return 1;

	if (col == N) 
	{
		row++;
		col = 0;
	}

	if (a[row][col] > 0)
		return solveSuduko(row, col + 1);

	for (int num = 1; num <= N; num++) 
	{
		
		// Check if it is safe to place 
		// the num (1-9) in the
		// given row ,col ->we move to next column
		if (isSafe(passer, row, col, num)==1) 
		{
			/* assigning the num in the 
			current (row,col)
			position of the grid
			and assuming our assined num 
			in the position
			is correct	 */
			a[row][col] = num;
		
			// Checking for next possibility with next
			// column
			if (solveSuduko( row, col + 1)==1)
				return 1;
		}
	
		// Removing the assigned num ,
		// since our assumption
		// was wrong , and we go for next 
		// assumption with
		// diff num value
		a[row][col] = 0;
	}
   
	return 0;
}


//function to return answer to python gui
int *get_answer(int *x)
{
    int *q = (int*)malloc(sizeof(int)*81);
    
    for (int i = 0; i < 9; i++)
	{
		for (int j = 0; j < 9; j++)
		{
			a[i][j] = x[j%9+i*9];
		}
	}
    solveSuduko(0,0);
    for(int i=0;i<9;i++)
    {
        for(int j=0;j<9;j++)
        {
            q[i * 9 + j] = a[i][j] ;
        }
    }
    return q;
}