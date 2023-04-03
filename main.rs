use std::fs::{self, File};
use std::io::prelude::*;
use std::path::Path;
use std::env;
use std::time::Duration;
use std::sync::Arc;
use sevenz_rust::decompress_file_with_password;
use rayon::ThreadPoolBuilder;
use sysinfo::{System, SystemExt, ProcessExt};

const CPU_THRESHOLD: f32 = 90.0;

fn spawn_if_cpu_usage_low<F>(f: F) where F: FnOnce() + Send + 'static {
    Ok(cpu)=> {
        println!("\nMeasuring CPU load...");
        thread::sleep(Duration::from_secs(1));
        let cpu = cpu.done().unwrap();
        println!("CPU load: {}% user, {}% nice, {}% system, {}% intr, {}% idle ",
            cpu.user * 100.0, cpu.nice * 100.0, cpu.system * 100.0, cpu.interrupt * 100.0, cpu.idle * 100.0);
    },
    Err(x) => println!("\nCPU load: error: {}", x)
    if cpu.user < CPU_THRESHOLD {
        f();
    }
}

fn extract_malware_files(path: &str, extract_path: &str) {
    // Get a list of all the folders in the path
    let folders = fs::read_dir(path).expect("Failed to read path");

    let mut data: Vec<Vec<String>> = Vec::new();
    let start_time = std::time::Instant::now();

    // Loop through the folders
    for folder in folders {
        let folder_path = folder.unwrap().path();
        let folder_name = folder_path.file_name().unwrap().to_str().unwrap().to_owned();
        println!("Extracting {}", &folder_name);

        // Create a folder for the malware family
        let family_folder_path = Path::new(&extract_path).join(&folder_name);
        if !family_folder_path.exists() {
            fs::create_dir_all(&family_folder_path).expect("Failed to create family folder");
        }

        // Get a list of all the files in the folder
        let files = fs::read_dir(&folder_path).expect("Failed to read folder");

        // Create a thread pool for the tasks
        let pool = ThreadPoolBuilder::new()
            .num_threads(num_cpus::get())
            .build()
            .unwrap();

        // Convert the files to a vector
        let files: Vec<_> = files.collect();
        let files = Arc::new(files);
        let data = Arc::new(data);
        for i in 0..files.len() {
            let files = files.clone();
            let data = data.clone();
            spawn_if_cpu_usage_low(move || {
                let file = &files[i];
                let file_path = file.path();
                let file_name = file_path.file_name().unwrap().to_str().unwrap().to_owned();
                println!("Extracting {},{}", &file_name, &folder_name);

                // Check if the file is a 7z file
                if file_path.extension().unwrap() == "7z" {
                    // Check if the file has already been extracted
                    let filename = file_name.split(".").next().unwrap_or_default().to_owned();
                    if !family_folder_path.join(&filename).exists() {
                        // Extract the file with the password "infected"
                        decompress_file_with_password(&file_path, &family_folder_path, "infected".into())
                            .expect("Failed to extract file");
                    }

                    // Run the command to generate a png file of the malware
                    // Usage: D:\devwork\10dma\spectrum.exe <input_file_path> <output_file_path>
                    // Filename without the extension
                    let png_file_path = family_folder_path.join(&format!("{}.png", filename));
                    if !png_file_path.exists() {
                    let mut cmd = std::process::Command::new("D:\\devwork\\10dma\\spectrum.exe");
                    cmd.arg(file_path).arg(&png_file_path);
                    let output = cmd.output().expect("Failed to execute command");
                    if output.status.success() {
                    println!("Generated png for {}", &file_name);
                    } else {
                    println!(
                    "Error generating png for {}: {}",
                    &file_name,
                    String::from_utf8_lossy(&output.stderr)
                    );
                    }
                    }
                                    // Delete the extracted file
                fs::remove_file(family_folder_path.join(&filename));

                // Add the malware name, family, and extracted file path to the data list
                let row = vec![
                    file_name,
                    folder_name.clone(),
                    png_file_path.to_str().unwrap().to_owned(),
                ];

                let mut data = data.lock().unwrap();
                data.push(row);
            }
        });

        // Sleep for a short duration to prevent spawning too many workers quickly
        std::thread::sleep(Duration::from_millis(10));
    }

    // Wait for all tasks to complete
    pool.join();
}

let end_time = start_time.elapsed();
println!("Time taken: {:?}", end_time);

// Export the data to a csv file
let mut csv_file = File::create("malware_data.csv").expect("Failed to create csv file");
writeln!(csv_file, "Sample,Family,PNGFilePath").expect("Failed to write csv header");
for row in &data {
    writeln!(csv_file, "{}", row.join(",")).expect("Failed to write csv row");
}
}

fn main() {
// Check command-line arguments length
let args: Vec<String> = env::args().collect();
if args.len() != 3 {
eprintln!("Usage: {} <input_file_path> <output_file_path>", args[0]);
std::process::exit(1);
}
let path = &args[1];
let extract_path = &args[2];
extract_malware_files(path, extract_path);
}
                    
                    
