package main

import (
	"bytes"
	"image/color"
	"image/png"
	"math"
	"os"

	"gonum.org/v1/gonum/dsp/fourier"

	"github.com/mjibson/go-dsp/spectral"
	"github.com/mjibson/go-dsp/wav"
)

func main() {
	// Open the audio file
	f, err := os.Open("input.wav")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	// Read the audio data
	s, err := wav.New(f)
	if err != nil {
		panic(err)
	}

	// Get the number of samples and sample rate
	n := s.Samples
	fs := s.SampleRate

	// Compute the spectrogram
	spectrogram := spectral.Spectrogram(n, fs, fourier.WindowHamming, fourier.Forward, func(i int) float64 {
		return float64(s.Data[i]) / float64(math.MaxInt16)
	})

	// Create an image of the spectrogram
	img := spectral.Image(spectrogram, color.Gray{}, 256)

	// Save the image as PNG
	var buf bytes.Buffer
	err = png.Encode(&buf, img)
	if err != nil {
		panic(err)
	}

	// Write the image to a file
	f, err = os.Create("spectrogram.png")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	_, err = f.Write(buf.Bytes())
	if err != nil {
		panic(err)
	}
}
