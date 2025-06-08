<script lang="ts">
  $: innerWidth = 0;
  $: innerHeight = 0;
</script>

<svelte:window bind:innerWidth bind:innerHeight />

<div class="window-bar">
  <div class="window-icons">
    {#each ["#FC5753", "#FDBB40", "#36C84B"] as color}
      <div class="window-button" style="--window-button-bg: {color};"></div>
    {/each}
  </div>
  <span id="window-title" style="--title-width: {innerWidth * 0.5}px">
    Boh {#if innerWidth / innerHeight > 0.45}
      {#if innerWidth > innerHeight}em: Uma conversa sobre estruturas e dados{/if}
      | [ ▀ v ▀]{/if}</span
  >
</div>

<style>
  .window-bar {
    display: flex;
    flex-direction: row;
    width: 100%;
    align-items: center;
    background-color: rgba(85, 85, 85, 0.6);
    max-height: 10vmin;
    border-top-left-radius: inherit;
    border-top-right-radius: inherit;
  }

  .window-icons {
    display: flex;
    flex-direction: row;
    gap: 1.2em;
    margin-left: 1rem;
    margin-block: 1em;
    z-index: 1000;
  }

  .window-button {
    min-width: 0.8rem;
    min-height: 0.8rem;
    border-radius: 50%;
    background-color: var(--window-button-bg, #f0f0f0);
    cursor: pointer;
  }

  #window-title {
    font-family: "Roboto Mono", Inconsolata, monospace, sans-serif;
    font-size: 0.8rem;
    color: white;
    position: absolute;
    min-width: var(--title-width, 1%);
    right: 25%;
    font-weight: 700;
  }

  @media screen and (min-width: 1200px) {
    .window-bar {
      max-height: 5.5vmin;
    }
    .window-button {
      min-width: 1.2rem;
      min-height: 1.2rem;
    }

    #window-title {
      font-size: 1.1rem;
    }
  }

  @media screen and (min-width: 310px) {
    #window-title {
      left: 50%;
      right: auto;
      transform: translateX(-50%);
      text-align: center;
    }
  }
</style>
