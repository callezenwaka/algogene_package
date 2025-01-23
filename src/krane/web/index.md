# Home

## Hero Image
![Gene Sequence Demo](../assets/krane.gif)

## Downloads

Select and download the latest version for your platform, and start developing today.

### LTS
Below are the stable versions recommended for most users.

#### Download Options

- [Windows Installer](https://github.com/callezenwaka/krane/tree/windows)
  ![Windows Logo](windows-logo.svg)
  - Version: `krane-v1.1`

- [macOS Installer](https://github.com/callezenwaka/krane/tree/macOS)
  ![macOS Logo](macos-logo.svg)
  - Version: `krane-v1.1`

## Subscribe for Updates

Drop your email below to get notification about updates.

<form @submit.prevent="onSubscribe">
  <label for="subscribe" aria-label="Subscribe">Subscribe: </label>
  <input type="text" v-model="email" name="subscribe" id="subscribe" placeholder="Enter your email" @blur="onBlur($event)" />
  <button :class="{isValid: isValid}" type="submit" name="submit">
    <span v-if="isLoading">
      <svg class="spinner" viewBox="0 0 50 50">
        <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
      </svg>
    </span>
    <span v-else>Subscribe</span>
  </button>
</form>