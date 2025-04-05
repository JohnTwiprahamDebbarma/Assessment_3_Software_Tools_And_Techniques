using System;

namespace CS202Lab10
{
    public class Calculator
    {
        // Properties
        private double Number1 { get; set; }
        private double Number2 { get; set; }

        // Constructor
        public Calculator(double num1, double num2)
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

    public class Activity2
    {
        public static void Run()
        {
            Console.WriteLine("Running Activity 2: Basic Calculator");
            Console.WriteLine("----------------------------------");

            // Get input from user
            Console.Write("Enter first number: ");
            string? input1 = Console.ReadLine() ?? string.Empty;

            Console.Write("Enter second number: ");
            string? input2 = Console.ReadLine() ?? string.Empty;

            // Convert input to double
            if (double.TryParse(input1, out double num1) && double.TryParse(input2, out double num2))
            {
                // Create calculator object
                Calculator calc = new Calculator(num1, num2);

                // Perform operations and display results
                Console.WriteLine($"\nResults:");
                Console.WriteLine($"{num1} + {num2} = {calc.Add()}");
                Console.WriteLine($"{num1} - {num2} = {calc.Subtract()}");
                Console.WriteLine($"{num1} * {num2} = {calc.Multiply()}");
                Console.WriteLine($"{num1} / {num2} = {calc.Divide()}");

                // Check if sum is even or odd
                Console.WriteLine($"The sum {calc.Add()} is {calc.CheckSumEvenOrOdd()}");
            }
            else
            {
                Console.WriteLine("Invalid input. Please enter valid numbers.");
            }

            Console.WriteLine("\nPress any key to return to the menu...");
            Console.ReadKey();
        }
    }
}