// main.js for minimalistic 5-bar equalizer visualization and transitions
// This script is loaded in index.html

document.addEventListener('DOMContentLoaded', function () {
    // --- Minimalistic 5-Bar Equalizer Visualization ---
    const audio = document.getElementById('audioPlayer');
    const canvas = document.getElementById('visualizer');
    const equalizerVisualizer = document.getElementById('equalizerVisualizer');
    
    if (canvas && audio && equalizerVisualizer) {
        const ctx = canvas.getContext('2d');
        let audioCtx, analyser, src, dataArray, animationId;
        
        // Get the 5 equalizer bars
        const bars = document.querySelectorAll('.equalizer-bar');
        
        function resizeCanvas() {
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
        }
        
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();
        
        function setupAudioContext() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                src = audioCtx.createMediaElementSource(audio);
                analyser = audioCtx.createAnalyser();
                analyser.fftSize = 64; // Smaller FFT size for fewer frequency bins
                src.connect(analyser);
                analyser.connect(audioCtx.destination);
                dataArray = new Uint8Array(analyser.frequencyBinCount);
            }
        }
        
        function draw() {
            animationId = requestAnimationFrame(draw);
            
            if (!analyser) return;
            
            // Get frequency data for visualization
            analyser.getByteFrequencyData(dataArray);
            
            // Calculate average energy for subtle shadow effect
            let avgEnergy = 0;
            for (let i = 0; i < dataArray.length; i++) {
                avgEnergy += dataArray[i];
            }
            avgEnergy = avgEnergy / dataArray.length / 255;
            
            // Update the 5 equalizer bars
            // We'll use specific frequency ranges for each bar
            // Bar 1: Low bass
            // Bar 2: Mid bass
            // Bar 3: Mid range
            // Bar 4: High mid
            // Bar 5: High frequencies
            
            const frequencyRanges = [
                [0, 3],     // Low bass
                [4, 6],     // Mid bass
                [7, 10],    // Mid range
                [11, 15],   // High mid
                [16, 20]    // High frequencies
            ];
            
            // Update each bar based on its frequency range
            for (let i = 0; i < bars.length; i++) {
                const [startFreq, endFreq] = frequencyRanges[i];
                let sum = 0;
                
                // Calculate average value in the frequency range
                for (let j = startFreq; j <= endFreq; j++) {
                    sum += dataArray[j];
                }
                
                const average = sum / (endFreq - startFreq + 1);
                const percent = average / 255;
                
                // Scale height between 20% and 90% of container height
                const height = 20 + (percent * 70);
                bars[i].style.height = `${height}%`;
                
                // Add subtle shadow based on intensity
                const shadowIntensity = Math.min(10, percent * 15);
                bars[i].style.boxShadow = `0 ${2 + percent * 3}px ${shadowIntensity}px rgba(0, 0, 0, 0.2)`;
                
                // Add floating effect with slight vertical movement
                const floatOffset = -2 - (percent * 3);
                bars[i].style.transform = `translateY(${floatOffset}px)`;
            }
            
            // Add subtle shadow on canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            if (avgEnergy > 0.4) { // Only add shadow effect when energy is above threshold
                // Create shadow effect
                const shadowSize = avgEnergy * 10;
                ctx.shadowBlur = shadowSize;
                ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.shadowBlur = 0;
            }
        }
        
        audio.addEventListener('play', () => {
            setupAudioContext();
            draw();
            
            // Add active class to visualizer
            document.querySelector('.visualizer-container').classList.add('active');
        });
        
        audio.addEventListener('pause', () => {
            cancelAnimationFrame(animationId);
            
            // Reset bars to default wave pattern when paused
            const defaultHeights = [30, 50, 70, 50, 30];
            const defaultTransforms = ['-2px', '-3px', '-4px', '-3px', '-2px'];
            bars.forEach((bar, index) => {
                bar.style.height = `${defaultHeights[index]}%`;
                bar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.2)';
                bar.style.transform = `translateY(${defaultTransforms[index]})`;
            });
            
            // Remove active class
            document.querySelector('.visualizer-container').classList.remove('active');
        });
        
        audio.addEventListener('ended', () => {
            cancelAnimationFrame(animationId);
            
            // Reset bars to default wave pattern when ended
            const defaultHeights = [30, 50, 70, 50, 30];
            const defaultTransforms = ['-2px', '-3px', '-4px', '-3px', '-2px'];
            bars.forEach((bar, index) => {
                bar.style.height = `${defaultHeights[index]}%`;
                bar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.2)';
                bar.style.transform = `translateY(${defaultTransforms[index]})`;
            });
            
            // Remove active class
            document.querySelector('.visualizer-container').classList.remove('active');
        });
    }

    // --- Animated Transitions ---
    // Fade/slide for player section
    const playerSection = document.querySelector('.player-section');
    function animatePlayerTransition() {
        if (playerSection) {
            playerSection.classList.remove('opacity-0', 'translate-y-4');
            playerSection.classList.add('transition-all', 'duration-500', 'ease-in-out', 'opacity-100', 'translate-y-0');
        }
    }
    
    // On song change, fade out/in song info
    const nowPlaying = document.getElementById('nowPlaying');
    function animateSongChange() {
        if (nowPlaying) {
            nowPlaying.classList.add('transition-opacity', 'duration-300', 'opacity-0');
            setTimeout(() => {
                nowPlaying.classList.remove('opacity-0');
                nowPlaying.classList.add('opacity-100');
            }, 300);
        }
    }

    // Patch playSong to animate song info
    if (window.playSong) {
        const origPlaySong = window.playSong;
        window.playSong = function () {
            animateSongChange();
            origPlaySong.apply(this, arguments);
        };
    }

    // On page load, animate player
    animatePlayerTransition();
});
