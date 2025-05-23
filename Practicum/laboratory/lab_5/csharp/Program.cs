using System;
using System.Diagnostics;
using System.IO;
using System.Globalization;
using CsvHelper;
using System.Linq;

namespace lab5Integration
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                string[] scripts = new[]
                {
                    @"C:/Users/motyn/Desktop/Repositories/OMSTU/Practicum/laboratory/lab_5/process/preprocess.py",
                    @"C:/Users/motyn/Desktop/Repositories/OMSTU/Practicum/laboratory/lab_5/process/generate_new_data.py",
                    @"C:/Users/motyn/Desktop/Repositories/OMSTU/Practicum/laboratory/lab_5/scripts/train_logreg.py",
                    @"C:/Users/motyn/Desktop/Repositories/OMSTU/Practicum/laboratory/lab_5/scripts/train_nb.py",
                    @"C:/Users/motyn/Desktop/Repositories/OMSTU/Practicum/laboratory/lab_5/scripts/train_svm.py",
                    @"C:/Users/motyn/Desktop/Repositories/OMSTU/Practicum/laboratory/lab_5/scripts/run_all.py"
                };

                foreach (var script in scripts)
                {
                    RunPythonScript(script);
                }

                string csvPath = @"C:/Users/motyn/Desktop/Repositories/OMSTU/Practicum/laboratory/lab_5/data/model_results.csv";
                DisplayCsv(csvPath);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Ошибка: " + ex.Message);
            }
        }

        static void RunPythonScript(string scriptPath)
        {
            Console.WriteLine($"\n▶ Выполнение: {scriptPath}");
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = @"C:\Users\motyn\AppData\Local\Programs\Python\Python311\python.exe",
                    Arguments = $"\"{scriptPath}\"",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                }
            };

            process.Start();
            string output = process.StandardOutput.ReadToEnd();
            string error = process.StandardError.ReadToEnd();
            process.WaitForExit();

            Console.WriteLine(output);
            if (!string.IsNullOrEmpty(error))
                Console.WriteLine("⚠ Ошибка: " + error);
        }

        static void DisplayCsv(string csvPath)
        {
            if (!File.Exists(csvPath))
            {
                Console.WriteLine("❌ CSV не найден: " + csvPath);
                return;
            }

            Console.WriteLine("\n📊 Результаты моделей:");
            using (var reader = new StreamReader(csvPath))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                var records = csv.GetRecords<dynamic>().ToList();
                foreach (var row in records)
                {
                    foreach (var kv in row)
                        Console.Write($"{kv.Key}: {kv.Value} | ");
                    Console.WriteLine();
                }
            }
        }
    }
}
