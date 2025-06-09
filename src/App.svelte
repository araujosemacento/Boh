<script lang="ts">
  import Windowbar from "./lib/Windowbar.svelte";
  $: innerWidth = 0;
  $: innerHeight = 0;
</script>

<svelte:window bind:innerWidth bind:innerHeight />

<main>
  <div class="terminal">
    <Windowbar {innerWidth} {innerHeight} />
    <div class="board">
      <p class="talk">
        <span id="boh">[ ▀ ─ ▀]</span> <span class="bubble">──</span><span
          id="line"
          lang="pt-BR"
          >Tô só te esperando, tá bom?<span id="carret">█</span></span
        >
      </p>
    </div>
  </div>
</main>

<style>
  .terminal {
    width: 90vw;
    height: 95vh;
    background-color: #111;
    color: white;
    font-family: monospace;
    display: flex;
    flex-direction: column;
    border-radius: 10px;
    align-self: center;
    justify-self: center;
    box-shadow: 0 0 100px rgba(50, 10, 50, 0.9);
  }
  .board {
    display: flex;
    flex-grow: 1;
    max-width: 100%;
    max-height: 100%;
    flex-direction: column;
  }
  .talk {
    display: flex;
    font-size: 1.2em;
    flex-direction: row;
    margin-left: 10%;
    margin-top: 10vmax;
  }
  #boh {
    color: #28e;
    font: "Cultive Mono", monospace, serif;
    font-weight: 700;
    min-width: fit-content;
  }
  #line {
    color: #fff;
    font-weight: 500;
    transform: translateY(-0.1em);
    text-align: justify-all;
    text-wrap-mode: unset;
    width: 50%;
    padding-inline: 0.333em;
    border-inline: 0.125em solid #82f;
    hyphens: auto;
    -webkit-hyphens: auto;
    -moz-hyphens: auto;
    -ms-hyphens: auto;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }
  .bubble {
    color: #82f;
    font-weight: 700;
  }
  #carret {
    animation: blink 1.5s infinite;
    margin-left: 0.25em;
  }
  @media screen and (orientation: landscape) {
    .terminal {
      width: 90vw;
      height: 90vh;
    }
    .talk {
      margin-top: 10vmin;
    }
    #line {
      width: fit-content;
    }
  }
  @media screen and (min-width: 1024px) {
    .terminal {
      width: 70vw;
      height: 80vh;
    }
  }

  @keyframes blink {
    0%,
    60% {
      opacity: 1;
    }
    64%,
    96% {
      opacity: 0;
    }
  }
</style>
