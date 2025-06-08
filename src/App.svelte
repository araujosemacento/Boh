<script lang="ts">
  // @ts-ignore
  import Windowbar from "/src/lib/Windowbar.svelte";
</script>

<main>
  <div class="terminal">
    <Windowbar />
  </div>
</main>

<style>
  .terminal {
    min-width: 90vw;
    min-height: 95vh;
    background-color: #050010;
    color: white;
    font-family: monospace;
    display: flex;
    flex-direction: column;
    border-radius: 10px;
    align-self: center;
    justify-self: center;
    box-shadow: 0 0 100px rgba(50, 10, 50, 0.9);
  }
  @media screen and (orientation: landscape) {
    .terminal {
      min-width: 90vw;
      min-height: 90vh;
    }
  }
  @media screen and (min-width: 1024px) {
    .terminal {
      min-width: 70vw;
      min-height: 80vh;
    }
  }
</style>
