using System;

namespace CS202Lab10
{
    public class Activity6
    {
        public static void Run()
        {
            Console.WriteLine("Running Activity 6: Debugging with Visual Studio");
            Console.WriteLine("----------------------------------------------");
            Console.WriteLine("\nDebugging Instructions:");
            Console.WriteLine("1. Set breakpoints in the code by clicking in the left margin");
            Console.WriteLine("2. Run the program in Debug mode (F5)");
            Console.WriteLine("3. When execution hits a breakpoint:");
            Console.WriteLine("   - Use Step Into (F11) to enter method calls");
            Console.WriteLine("   - Use Step Over (F10) to execute current line");
            Console.WriteLine("   - Use Step Out (Shift+F11) to exit current method");
            Console.WriteLine("4. Hover over variables to see their values");
            Console.WriteLine("5. Use Watch window to monitor specific variables");

            Console.WriteLine("\nFor this lab, we should take screenshots of:");
            Console.WriteLine("- Breakpoints in your code");
            Console.WriteLine("- Variables during debugging");
            Console.WriteLine("- Call stack during method execution");
            Console.WriteLine("- Examples of Step-in, Step-over, and Step-out");

            Console.WriteLine("\nPress any key to return to the menu...");
            Console.ReadKey();
        }
    }
}
