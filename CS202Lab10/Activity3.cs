using System;

namespace CS202Lab10
{
    public class MathOperations
    {
        // Method to print numbers from 1 to 10 using for loop
        public void PrintNumbers()
        {
            Console.WriteLine("\nPrinting numbers from 1 to 10 using for loop:");
            for (int i = 1; i <= 10; i++)
            {
                Console.Write($"{i} ");
            }
            Console.WriteLine();
        }

        // Method to calculate factorial of a number
        public long CalculateFactorial(int number)
        {
            if (number < 0)
                throw new ArgumentException("Factorial is not defined for negative numbers.");

            if (number == 0 || number == 1)
                return 1;

            long factorial = 1;
            for (int i = 2; i <= number; i++)
            {
                factorial *= i;
            }

            return factorial;
        }

        // Method to process user input until "exit" is entered
        public void ProcessUserInput()
        {
            string input = "";

            Console.WriteLine("\nEnter a number to calculate its factorial or 'exit' to quit:");

            while (input.ToLower() != "exit")
            {
                Console.Write("> ");
                input = Console.ReadLine() ?? string.Empty;

                if (input.ToLower() == "exit")
                    break;

                if (int.TryParse(input, out int number))
                {
                    try
                    {
                        long result = CalculateFactorial(number);
                        Console.WriteLine($"Factorial of {number} is {result}");
                    }
                    catch (ArgumentException ex)
                    {
                        Console.WriteLine(ex.Message);
                    }
                    catch (OverflowException)
                    {
                        Console.WriteLine("Result is too large to calculate.");
                    }
                }
                else
                {
                    Console.WriteLine("Invalid input. Please enter a valid number or 'exit'.");
                }
            }
        }
    }

    public class Activity3
    {
        public static void Run()
        {
            Console.WriteLine("Running Activity 3: Loops and Functions");
            Console.WriteLine("--------------------------------------");

            MathOperations mathOps = new MathOperations();

            // Print numbers using for loop
            mathOps.PrintNumbers();

            // Process user input using while loop and calculate factorial
            mathOps.ProcessUserInput();

            Console.WriteLine("\nPress any key to return to the menu...");
            Console.ReadKey();
        }
    }
}
