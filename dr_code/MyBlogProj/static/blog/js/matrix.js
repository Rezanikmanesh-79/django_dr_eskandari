// Matrix Rain Effect
function createMatrixRain() {
    const matrixBg = document.getElementById('matrixBg');
    const characters = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
    
    function createColumn() {
        const column = document.createElement('div');
        column.className = 'matrix-column';
        column.style.left = Math.random() * window.innerWidth + 'px';
        column.style.animationDuration = (Math.random() * 3 + 2) + 's';
        column.style.opacity = Math.random();
        
        let text = '';
        for (let i = 0; i < Math.floor(Math.random() * 20) + 10; i++) {
            text += characters.charAt(Math.floor(Math.random() * characters.length)) + '<br>';
        }
        column.innerHTML = text;
        
        matrixBg.appendChild(column);
        
        setTimeout(() => {
            if (column.parentNode) {
                column.parentNode.removeChild(column);
            }
        }, 5000);
    }
    
    // Create initial columns
    for (let i = 0; i < 50; i++) {
        setTimeout(createColumn, i * 100);
    }
    
    // Continue creating columns
    setInterval(createColumn, 200);
}

// Smooth scroll to posts
function scrollToPosts() {
    document.getElementById('posts').scrollIntoView({
        behavior: 'smooth'
    });
}

// Terminal cursor animation
function animateTerminalCursor() {
    const cursor = document.querySelector('.cursor');
    if (cursor) {
        setInterval(() => {
            cursor.style.opacity = cursor.style.opacity === '0' ? '1' : '0';
        }, 500);
    }
}

// Glitch effect for logo
function addGlitchEffect() {
    const logo = document.querySelector('.logo');
    setInterval(() => {
        if (Math.random() < 0.1) {
            logo.style.textShadow = '2px 0 #ff0000, -2px 0 #00ffff';
            setTimeout(() => {
                logo.style.textShadow = '0 0 10px #00ff00';
            }, 100);
        }
    }, 2000);
}

// Add typing effect to blog post titles on scroll
function addScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'glow 2s ease-in-out infinite alternate';
            }
        });
    });

    document.querySelectorAll('.post-title').forEach(title => {
        observer.observe(title);
    });
}

// Terminal typing effect
function addTerminalTyping() {
    const terminalLines = document.querySelectorAll('.terminal-prompt, .terminal-output');
    let delay = 0;
    
    terminalLines.forEach(line => {
        const text = line.textContent;
        line.textContent = '';
        line.style.opacity = '0';
        
        setTimeout(() => {
            line.style.opacity = '1';
            let i = 0;
            const typeInterval = setInterval(() => {
                line.textContent += text[i];
                i++;
                if (i >= text.length) {
                    clearInterval(typeInterval);
                }
            }, 50);
        }, delay);
        
        delay += text.length * 50 + 500;
    });
}

// Random matrix characters in background
function addRandomMatrixChars() {
    const chars = '01';
    const body = document.body;
    
    setInterval(() => {
        if (Math.random() < 0.3) {
            const char = document.createElement('span');
            char.textContent = chars[Math.floor(Math.random() * chars.length)];
            char.style.position = 'fixed';
            char.style.left = Math.random() * window.innerWidth + 'px';
            char.style.top = Math.random() * window.innerHeight + 'px';
            char.style.color = '#00ff00';
            char.style.fontSize = '12px';
            char.style.opacity = '0.3';
            char.style.pointerEvents = 'none';
            char.style.zIndex = '1';
            char.style.fontFamily = 'Courier New, monospace';
            
            body.appendChild(char);
            
            setTimeout(() => {
                char.style.opacity = '0';
                setTimeout(() => {
                    if (char.parentNode) {
                        char.parentNode.removeChild(char);
                    }
                }, 1000);
            }, 2000);
        }
    }, 1000);
}

// Hacker text scramble effect
function scrambleText(element, finalText, duration = 2000) {
    const chars = '!@#$%^&*()_+-=[]{}|;:,.<>?01';
    const steps = 20;
    const stepDuration = duration / steps;
    let step = 0;
    
    const interval = setInterval(() => {
        let scrambled = '';
        for (let i = 0; i < finalText.length; i++) {
            if (i < step) {
                scrambled += finalText[i];
            } else {
                scrambled += chars[Math.floor(Math.random() * chars.length)];
            }
        }
        element.textContent = scrambled;
        
        step++;
        if (step > finalText.length) {
            clearInterval(interval);
            element.textContent = finalText;
        }
    }, stepDuration);
}

// Add hacker-style loading effect
function addLoadingEffect() {
    const loadingTexts = [
        'Initializing Matrix Protocol...',
        'Connecting to mainframe...',
        'Bypassing security systems...',
        'Access granted. Welcome to the Matrix.'
    ];
    
    let currentIndex = 0;
    const loadingElement = document.createElement('div');
    loadingElement.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0, 0, 0, 0.9);
        color: #00ff00;
        padding: 2rem;
        border: 2px solid #00ff00;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        z-index: 9999;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
    `;
    
    document.body.appendChild(loadingElement);
    
    function showNextText() {
        if (currentIndex < loadingTexts.length) {
            scrambleText(loadingElement, loadingTexts[currentIndex], 1000);
            currentIndex++;
            setTimeout(showNextText, 1500);
        } else {
            loadingElement.style.opacity = '0';
            setTimeout(() => {
                if (loadingElement.parentNode) {
                    loadingElement.parentNode.removeChild(loadingElement);
                }
            }, 500);
        }
    }
    
    showNextText();
}

// Initialize all effects
document.addEventListener('DOMContentLoaded', function() {
    // Show loading effect first
    addLoadingEffect();
    
    // Initialize other effects after loading
    setTimeout(() => {
        createMatrixRain();
        animateTerminalCursor();
        addGlitchEffect();
        addScrollAnimations();
        addRandomMatrixChars();
        
        // Add terminal typing effect after a delay
        setTimeout(addTerminalTyping, 2000);
    }, 6000);
});

// Handle window resize for matrix effect
window.addEventListener('resize', function() {
    // Clear existing columns and recreate
    const matrixBg = document.getElementById('matrixBg');
    if (matrixBg) {
        matrixBg.innerHTML = '';
        setTimeout(createMatrixRain, 100);
    }
});

// Add keyboard shortcuts for hacker feel
document.addEventListener('keydown', function(e) {
    // Ctrl + Shift + M for Matrix mode
    if (e.ctrlKey && e.shiftKey && e.key === 'M') {
        e.preventDefault();
        const body = document.body;
        body.style.filter = body.style.filter === 'invert(1)' ? 'none' : 'invert(1)';
    }
    
    // Escape key to clear effects
    if (e.key === 'Escape') {
        const matrixBg = document.getElementById('matrixBg');
        if (matrixBg) {
            matrixBg.innerHTML = '';
        }
    }
});

// Add mouse trail effect
let mouseTrail = [];
document.addEventListener('mousemove', function(e) {
    mouseTrail.push({x: e.clientX, y: e.clientY, time: Date.now()});
    
    // Keep only recent trail points
    mouseTrail = mouseTrail.filter(point => Date.now() - point.time < 1000);
    
    // Create trail effect occasionally
    if (Math.random() < 0.1) {
        const trail = document.createElement('div');
        trail.style.cssText = `
            position: fixed;
            left: ${e.clientX}px;
            top: ${e.clientY}px;
            width: 2px;
            height: 2px;
            background: #00ff00;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            opacity: 0.7;
        `;
        
        document.body.appendChild(trail);
        
        setTimeout(() => {
            trail.style.opacity = '0';
            setTimeout(() => {
                if (trail.parentNode) {
                    trail.parentNode.removeChild(trail);
                }
            }, 500);
        }, 200);
    }
});