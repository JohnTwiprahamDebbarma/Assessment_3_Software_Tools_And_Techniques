using System;
using System.Diagnostics;

namespace CS202Lab10
{
    class Program
    {
        static void Main(string[] args)
        {
            bool exitProgram = false;

            while (!exitProgram)
            {
                Console.Clear();
                Console.WriteLine("CS202 Lab 10 - C# Console Applications");
                Console.WriteLine("======================================");
                Console.WriteLine("\nChoose an activity to run:");
                Console.WriteLine("1. Activity 1: Setting Up .NET Environment");
                Console.WriteLine("2. Activity 2: Basic Calculator (Syntax and Control Structures)");
                Console.WriteLine("3. Activity 3: Loops and Functions");
                Console.WriteLine("4. Activity 4: Object-Oriented Programming");
                Console.WriteLine("5. Activity 5: Exception Handling");
                Console.WriteLine("6. Activity 6: Debugging Guide");
                Console.WriteLine("0. Exit Program");

                Console.Write("\nEnter your choice [0-6]: ");
                string? choice = Console.ReadLine() ?? string.Empty;
                Console.Clear();

                switch (choice)
                {
                    case "1":
                        Activity1.Run();
                        break;
                    case "2":
                        Activity2.Run();
                        break;
                    case "3":
                        Activity3.Run();
                        break;
                    case "4":
                        Activity4.Run();
                        break;
                    case "5":
                        Activity5.Run();
                        break;
                    case "6":
                        Activity6.Run();
                        break;
                    case "0":
                        exitProgram = true;
                        Console.WriteLine("Thank you for using my lab assignment program. Goodbye!");
                        break;
                    default:
                        Console.WriteLine("Invalid option. Press any key to try again...");
                        Console.ReadKey();
                        break;
                }
            }
        }
    }
}
