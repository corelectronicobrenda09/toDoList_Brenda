Console.Write("Nombre: ");
string nombre = Console.ReadLine();

Console.Write("Apellido: ");
string apellido = Console.ReadLine();

Console.Write("Edad: ");
int edad = int.Parse(Console.ReadLine());

Console.Write("Altura: ");
float altura = float.Parse(Console.ReadLine());

Console.WriteLine($"\nHola, mi nombre es {nombre} {apellido}, tengo {edad} años y mido {altura}.");