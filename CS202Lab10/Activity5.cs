using System;

namespace CS202Lab10
{
    public class CalculatorWithExceptionHandling
    {
        // Properties
        private double Number1 { get; set; }
        private double Number2 { get; set; }
        
        // Constructor
        public CalculatorWithExceptionHandling(double num1, double num2)
        {
            Number1 = num1;
            Number2 = num2;
        }

        // Methods for arithmetic operations
        public double Add()
        {
            return Number1 + Number2;
        }

        public double Subtract()
        {
            return Number1 - Number2;
        }

        public double Multiply()
        {
            return Number1 * Number2;
        }

        public double Divide()
        {
            // Check for division by zero
            if (Number2 == 0)
            {
                throw new DivideByZeroException("Cannot divide by zero.");
            }
            return Number1 / Number2;
        }

        // Method to check if sum is even or odd
        public string CheckSumEvenOrOdd()
        {
            double sum = Add();
            if (sum % 2 == 0)
                return "even";
            else
                return "odd";
        }
    }

    public class Activity5
    {
        public static void Run()
        {
            Console.WriteLine("Running Activity 5: Exception Handling");
            Console.WriteLine("-------------------------------------");

            try
            {
                // Get input from user with exception handling
                Console.Write("Enter first number: ");
                string? input1 = Console.ReadLine() ?? string.Empty;

                Console.Write("Enter second number: ");
                string? input2 = Console.ReadLine() ?? string.Empty;

                // Parse input with exception handling
                double num1, num2;

                if (!double.TryParse(input1, out num1))
                {
                    throw new FormatException("First input is not a valid number.");
                }

                if (!double.TryParse(input2, out num2))
                {
                    throw new FormatException("Second input is not a valid number.");
                }

                // Create calculator object
                CalculatorWithExceptionHandling calc = new CalculatorWithExceptionHandling(num1, num2);

                // Perform operations and display results with exception handling
                Console.WriteLine($"\nResults:");
                Console.WriteLine($"{num1} + {num2} = {calc.Add()}");
                Console.WriteLine($"{num1} - {num2} = {calc.Subtract()}");
                Console.WriteLine($"{num1} * {num2} = {calc.Multiply()}");

                try
                {
                    double divisionResult = calc.Divide();
                    Console.WriteLine($"{num1} / {num2} = {divisionResult}");
                }
                catch (DivideByZeroException ex)
                {
                    Console.WriteLine($"Division Error: {ex.Message}");
                }

                // Check if sum is even or odd
                Console.WriteLine($"The sum {calc.Add()} is {calc.CheckSumEvenOrOdd()}");
            }
            catch (FormatException ex)
            {
                Console.WriteLine($"Input Error: {ex.Message}");
            }
            catch (OverflowException)
            {
                Console.WriteLine("Input Error: The number is too large or too small.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Unexpected Error: {ex.Message}");
            }

            Console.WriteLine("\nPress any key to return to the menu...");
            Console.ReadKey();
        }
    }
}
