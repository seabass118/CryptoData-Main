particlesJS("particles-js", {
    "particles": {
        "number": {
        "value": 10,
        "density": {
            "enable": true,
            "value_area": 500
        }
        },
        "color": {
        "value": "#00ff89"
        },
        "shape": {
        "type": "edge",
        "stroke": {
            "width": 0,
            "color": "00ff89"
        },
        "polygon": {
            "nb_sides": 5
        },
        },
        "opacity": {
        "value": 0.5,
        "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.1,
            "sync": true
        }
        },
        "size": {
        "value": 10,
        "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
        }
        },
        "line_linked": {
        "enable": true,
        "distance": 100,
        "color": "#fff",
        "opacity": 1,
        "width": 1
        },
        "move": {
        "enable": true,
        "speed": 5,
        "direction": "straight",
        "straight": false,
        "attract": {
            "enable": true,
            "rotateX": 1000,
            "rotateY": 1200
        }
        }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": {
        "onhover": {
            "enable": true,
            "mode": "grab"
        },
        "onclick": {
            "enable": true,
            "mode": "push"
        },
        "resize": true
        },
        "modes": {
        "grab": {
            "distance": 140,
            "line_linked": {
            "opacity": 1
            }
        },
        "bubble": {
            "distance": 400,
            "size": 40,
            "duration": 2,
            "opacity": 8,
            "speed": 3
        },
        "repulse": {
            "distance": 200,
            "duration": 0.4
        },
        "push": {
            "particles_nb": 4
        },
        "remove": {
            "particles_nb": 2
        }
        }
    },
    "retina_detect": true
    });


    /* ---- stats.js config ---- */

    var count_particles, stats, update;
    document.body.appendChild(stats.domElement);
    count_particles = document.querySelector('.js-count-particles');
    update = function() {
    stats.begin();
    stats.end();
    if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) {
        count_particles.innerText = window.pJSDom[0].pJS.particles.array.length;
    }
    requestAnimationFrame(update);
    };
    requestAnimationFrame(update);