<template>
    <div>
        <canvas :id="title" ref="context"></canvas>
    </div>
</template>

<script>
    import { ref, onMounted } from "vue";
    import Chart from 'chart.js/auto';
    import { getRelativePosition } from 'chart.js/helpers'; 

    export default {
        props: {
            title: String,
            labels: Array,
            label: String,
            dataset: Array,
            type: String,
        },
        setup(props) {
            // setup() receives props as the first argument.
            const context = ref();

            const labels = props.labels;
            const data = {
                labels,
                datasets: [{
                    label: props.label,
                    data: props.dataset,
                    backgroundColor: ["rgb(238, 173, 45)", "rgb(190, 138, 36)", "rgb(238, 173, 45)", "rgb(230, 194, 124)", "rgb(113, 83, 30)", "rgb(75, 56, 24)", "rgb(41, 31, 16)"]
                }]
            };

            const config = {
                type: props.type,
                data: data,
                options: {
                    responsive: true,
                    scales: {
                    r: {
                        pointLabels: {
                        display: true,
                        centerPointLabels: true,
                        font: {
                            size: 10
                        }
                        }
                    }
                    },
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: props.title
                        }
                    }
                },
            }

        
            onMounted(() => {
                const ctx = document.getElementById(props.title);
                const chart = new Chart(ctx, config);
                chart;
            });

            return {
                context
            }
        }
    }
</script>