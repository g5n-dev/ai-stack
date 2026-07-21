---
title: "Custom OS installation now available on AWS DeepRacer devices"
date: 2026-07-21T17:43:08+08:00
draft: false
entry_kind: "auto"
tags: ["Announcements", "AWS DeepRacer", "Intermediate (200)", "博客与播客", "来源快报"]
categories: []
source: "blogs_podcasts"
content_mode: "source_brief"
publication_tier: "C"
source_capture_mode: "excerpt"
source_snapshot_sha256: "sha256:8927650262ca1131888e469a3ad0b7b43ff35877afa3a63aae216a2a3de20ed4"
source_payload_sha256: "sha256:5e00082f5ca6bd0af4af15b04cd3cbfff484e2293eaacb3af7700393d502fec6"
observation_id: obs_af9d12402f049ccc28aff62be3f4ba73ef8a5523e75e9787004d4f7dcca9700f
event_id: evt_f83363fbd9108120f5f2ac3972af649054c947f68d279b72e87c8e3be16f489d
revision_id: rev_d64a2b9c430354d3b8d9952b4ab09b9e2bacf8c70081f29d5c52ce2326ca6184
source_published_at: 2026-07-20T17:25:24Z
first_seen_at: 2026-07-21T10:01:01Z
timestamp_confidence: feed
lineage_relation: original
extractor_version: "source-contract-v1"
discovery_method: "rss_excerpt"
source_completeness: "partial"
source_is_truncated: false
source_support: 1.0
source_title_chars_original: 61
description: "当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。"
external_url: https://aws.amazon.com/blogs/machine-learning/custom-os-installation-now-available-on-aws-deepracer-devices
parent_observation_id: null
last_seen_at: 2026-07-21T09:42:27.846031Z
---

## 基本信息

- **来源**: blogs_podcasts
- **原始来源**: [https://aws.amazon.com/blogs/machine-learning/custom-os-installation-now-available-on-aws-deepracer-devices](https://aws.amazon.com/blogs/machine-learning/custom-os-installation-now-available-on-aws-deepracer-devices)

## 来源摘要/节选

> With the stock firmware and software, developers couldn’t modify their AWS DeepRacer devices to use the latest operating systems. Now, developers can upgrade or install a custom operating system (OS) by using a newly released bootloader, which extends the life of these hardware devices.
>
> AWS DeepRacer devices are fully autonomous 1/18th scale race cars driven by models trained through reinforcement learning. These hardware devices, when paired with a cloud environment for training and evaluation of neural network models, provide an education and development environment intended to help developers get started with machine learning. As shipped, secure firmware on the AWS DeepRacer devices boots AWS-signed operating systems, including versions of Ubuntu 16.04 and 20.04. These versions of Ubuntu are no longer supported, making ongoing experimentation and research difficult. To keep these devices useful as long as possible, you need a way to authorize custom and modified software to run.
>
> With our developer bootloader, you can install custom operating systems outside of those originally provided. You can also install modern Linux distributions, add custom hardware drivers, run custom and more modern software stacks, build novel educational projects, and develop prototypes for new vehicle algorithms. In this post, we introduce the bootloader, discuss how to use it, and share links to a community distribution that uses it.
>
> Our solution
>
> Our team developed a bootloader that provides self-service developer access. The bootloader is based on the open-source shim project. With this developer shim, you can install custom or third-party distributions onto your AWS DeepRacer device.
>
> The developer shim targets developers familiar with Linux boot processes and certificate management. It’s particularly valuable for community members who want to create and distribute custom AWS DeepRacer installation distributions and media.
>
> On bootup, the developer shim blinks “DEVELOPER MODE” in Morse code on the AWS DeepRacer device’s built-in lights. After completing this indicator, the shim transfers control to the installed OS. The intent is for transparency through clear visual indicators whenever developer mode is active. These indicators help you understand your device’s security posture.
>
> Should you need to return to the original configuration, the process is completely reversible. You can follow the directions for Update Your Vehicle to return the device to stock configuration.
>
> The developer shim works through three key elements:
>
> 1. Self-service certificate management
>
> When built-in signature verification fails, the developer shim checks for developer certificates in /EFI/DEVELOPER/certs/ on the device’s boot partition. You can manage your own certificates using standard tools (OpenSSL, sbsign) while maintaining proper cryptographic verification.
>
> 2. Clear visual warnings
>
> When developer certificates are in use, the system provides a clear indication:
>
> On-screen warning (through HDMI) – Informs you of developer mode.
>
> Hardware indication – Device lights blink “DEVELOPER MODE” in Morse code.
>
> Boot delay – Gives you time to observe the developer mode activation.
>
> 3. Standard verification workflow
>
> The solution uses standard certificate-based signing tools, making it accessible to developers already working with secure boot processes. With this method, you can provide your own certificates while maintaining the cryptographic integrity of the boot chain and operating system.
>
> Community impact
>
> The open source AWS DeepRacer community at deepracing.io used this developer shim to create a new custom distribution for AWS DeepRacer devices, built on an Ubuntu 24.04 / ROS2 Jazzy software stack and featuring a Cloudscape-based user interface. As a practical demonstration of the self-service bootloader approach, it offers a ready-to-use solution for developers who want to get started quickly.
>
> Pre-packaged and using an installation process very similar to the original AWS distribution, it comes ready to deploy out of the box. The community prioritized racing performance, removing non-essential packages, including the X Window System graphical interface. You can add the desktop experience back in yourself if needed. Refer to the README for installation instructions.
>
> The developer shim allows the DeepRacing community to maintain and distribute updated software for AWS DeepRacer devices, extending their useful life well beyond the original distributions. The distribution can be found at https://github.com/aws-deepracer-community/deepracer-custom-car.
>
> How to use it
>
> You can use the bootloader with your AWS DeepRacer device across multiple usage patterns. You can upgrade using a community distribution, use a standard third-party OS, or even create your own custom OS. The exact steps depend on your choice.
>
> Option A: Install a community distribution
>
> You can get started by installing a community distribution, such as the Ubuntu 24.04 Community Distribution. This option provides an installation method without requiring the developer to custom install Linux and reconfigure its boot processes.
>
> Option B: Third-party distributions
>
> You can use the developer shim when installing a third-party distribution such as Ubuntu. Choose this option if you want control over the installation process. After installing the OS, replace the BOOTX64.EFI file with the developer shim and add the appropriate certificates. This might need to be done twice: once for the installation media, and again after installation. Consult the USAGE.md file in the developer shim package for guidance.
>
> Option C: Custom OS
>
> If you’re building a custom OS for the AWS DeepRacer device, create a boot volume on the device. Place the developer shim under EFI/BOOT/BOOTX64.EFI and your OS kernel or bootloader as EFI/BOOT/GRUBX64.EFI. Then install your public certificate under the DEVELOPER/certs path. Consult the USAGE.md file in the developer shim package for guidance.
>
> What to expect during early boot sequence
>
> The device goes through several stages on boot. Upon power-on, the device firmware loads the developer shim (BOOTX64.EFI) and transfers execution to it. The shim then displays a warning on the screen (when an HDMI monitor is attached) and blinks “DEVELOPER MODE” in Morse code on the device’s lights. This stage takes approximately 21 seconds. Much like the original firmware’s bootloader or a shim bootloader on a standard PC install, the developer bootloader then loads the operating system’s kernel. However, unlike the firmware, the developer bootloader checks the signature of this kernel against a local customizable certificate store kept in /EFI/DEVELOPER/certs. If the signature matches, the developer shim transfers execution to this operating system kernel, and boot continues normally.
>
> Pairing with self-managed AWS DeepRacer
>
> With the bootloader shim and the self-managed solution released on January 26, 2026, you now have full control over both the cloud-based training environments and your physical devices. Developers can customize the on-device software stack, experiment with new ROS2 packages, and iterate on racing models with total end-to-end flexibility. Visit DeepRacer on AWS for details on the self-managed solution.
>
> Getting started
>
> To get started, first explore the DeepRacer on AWS Solution and then download the developer shim at deepracer-developer-shim.zip. To create or modify the boot medium for the new custom operating system, place the BOOTX64.EFI shim file into the EFI/BOOT directory. Store your chosen operating system kernel as GRUBX64.EFI, and store the kernel’s public certificate in EFI/DEVELOPER/CERTS in x509 DER format. This might need to be done for both the operating system installation media and again on the device itself after installing from media. For more detailed technical documentation, troubleshooting, and advanced usage, refer to the bootloader’s USAGE.md file contained within the zip file.
>
> Alternatively, download the community distribution linked in the preceding How to use it section and follow the directions for a fresh install with the developer bootloader already incorporated.
>
> Conclusion
>
> Using the bootloader, you can unlock your AWS DeepRacer device and continue to use it as an education and development environment with the latest modern operating systems, tools, and software stacks. You can also customize your own operating system install or use community distributions.
>
> To get started, download the developer bootloader at deepracer-developer-shim.zip and follow the instructions in the USAGE.md file. After that, check out the Community Distribution and continue your machine learning (ML) journey with the DeepRacer on AWS Solution.
>
> With the flexibility introduced with the new bootloader, your imagination is the limit on what you can implement on the device. What will you build? Feel free to share on https://builder.aws.com/.
>
> About the authors
>
> Don Barber
>
> Don is a Senior Solutions Architect Manager working with AWS Strategic Accounts. Along with helping customers implement disruptive technology at scale, Don was an inaugural member of the AWS DeepRacer pitcrew, ran the first corporate league events, helped invent community racing and virtual live racing, and designed many of the AWS DeepRacer workshops, directly impacting thousands of developers to get started with AIML. Don is proud to help extend the lifespan of the AWS DeepRacer devices through this release.
>
> Lars Lorentz Ludvigsen
>
> Lars is a technology enthusiast who was introduced to AWS DeepRacer in late 2019 and was instantly hooked. Lars works as a Managing Director at Accenture, where he helps clients build the next generation of smart connected products. In addition to his role at Accenture, he’s an AWS Community Builder who focuses on developing and maintaining the AWS DeepRacer community’s software solutions. Lars’s AWS Community Builder blog is available at https://aws.amazon.com/blogs/machine-learning/author/larslorentzludvigsenamazon-com/.

## 来源说明

当前保存的是 RSS 或来源节选，不代表原文全文。请以原始来源为准。

> 本页只呈现已保存的来源证据，不包含基于缺失正文的扩展推断。