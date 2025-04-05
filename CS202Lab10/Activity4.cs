using System;

namespace CS202Lab10
{
    public class Student
    {
        // Properties with appropriate datatypes
        public string Name { get; set; } = string.Empty; // Initialize to avoid null warning
        public int ID { get; set; }
        public double Marks { get; set; }
        
        // Default constructor
        public Student()
        {
            Name = "Unknown";
            ID = 0;
            Marks = 0.0;
        }

        // Parameterized constructor
        public Student(string name, int id, double marks)
        {
            Name = name;
            ID = id;
            Marks = marks;
        }

        // Copy constructor
        public Student(Student other)
        {
            Name = other.Name;
            ID = other.ID;
            Marks = other.Marks;
        }

        // Method to determine grade based on marks
        public string getGrade()
        {
            if (Marks >= 90)
                return "A";
            else if (Marks >= 80)
                return "B";
            else if (Marks >= 70)
                return "C";
            else if (Marks >= 60)
                return "D";
            else if (Marks >= 50)
                return "E";
            else
                return "F";
        }

        // Method to display student details
        public virtual void DisplayDetails()
        {
            Console.WriteLine($"Student ID: {ID}");
            Console.WriteLine($"Name: {Name}");
            Console.WriteLine($"Marks: {Marks}");
            Console.WriteLine($"Grade: {getGrade()}");
        }
    }

    public class StudentIITGN : Student
    {
        // Additional property
        public string Hostel_Name_IITGN { get; set; } = string.Empty; // Initialize to avoid null warning

        // Default constructor
        public StudentIITGN() : base()
        {
            Hostel_Name_IITGN = "Unknown";
        }

        // Parameterized constructor
        public StudentIITGN(string name, int id, double marks, string hostelName)
            : base(name, id, marks)
        {
            Hostel_Name_IITGN = hostelName;
        }

        // Override method to display student details
        public override void DisplayDetails()
        {
            base.DisplayDetails();
            Console.WriteLine($"Hostel: {Hostel_Name_IITGN}");
        }
    }

    public class Activity4
    {
        public static void Run()
        {
            Console.WriteLine("Running Activity 4: Object-Oriented Programming");
            Console.WriteLine("---------------------------------------------");

            Console.WriteLine("Choose which demonstration to run:");
            Console.WriteLine("1. Regular Student Class");
            Console.WriteLine("2. IITGN Student Class");
            Console.Write("Enter your choice (1 or 2): ");

            string? choice = Console.ReadLine(); 
            Console.WriteLine();

            if (choice == "1")
            {
                // Create student using parameterized constructor
                Student student1 = new Student("John Debbarma", 101, 85.5);
                Console.WriteLine("Student 1 Details:");
                student1.DisplayDetails();

                Console.WriteLine();

                // Create student using copy constructor
                Student student2 = new Student(student1);
                student2.Name = "Ishiri Debbarma";  // Change name
                student2.ID = 102;           // Change ID
                Console.WriteLine("Student 2 Details (using Student 1):");
                student2.DisplayDetails();

                Console.WriteLine();

                // Create student using default constructor and set properties
                Student student3 = new Student();
                student3.Name = "Shiyari Debbarma";
                student3.ID = 103;
                student3.Marks = 92.0;
                Console.WriteLine("Student 3 Details:");
                student3.DisplayDetails();
            }
            else if (choice == "2")
            {
                // Create IITGN student
                StudentIITGN iitgnStudent = new StudentIITGN("John Debbarma", 201, 88.0, "Lekhaag");
                Console.WriteLine("IITGN Student Details:");
                iitgnStudent.DisplayDetails();
            }
            else
            {
                Console.WriteLine("Invalid choice. Running both demonstrations.");
                Console.WriteLine();

                // Run regular student demo
                Student student1 = new Student("Ishiri Debbarma", 101, 85.5);
                Console.WriteLine("Student 1 Details:");
                student1.DisplayDetails();

                Console.WriteLine("\n------------------------------------\n");

                // Run IITGN student demo
                StudentIITGN iitgnStudent = new StudentIITGN("John Debbarma", 201, 88.0, "Lekhaag");
                Console.WriteLine("IITGN Student Details:");
                iitgnStudent.DisplayDetails();
            }

            Console.WriteLine("\nPress any key to return to the menu...");
            Console.ReadKey();
        }
    }
}
