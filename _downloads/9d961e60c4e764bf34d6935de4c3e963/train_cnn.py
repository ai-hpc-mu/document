#!/usr/bin/env python3
"""Simple CNN Demo - CIFAR-10 Classification. Usage: python train_cnn.py --epochs 50 --batch_size 128 --lr 0.01"""
import argparse, csv, json, os, sys, time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(64*8*8, 256), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )
    def forward(self, x): return self.classifier(self.features(x))

def get_loaders(data_dir, batch_size):
    train_tf = transforms.Compose([transforms.RandomCrop(32, padding=4), transforms.RandomHorizontalFlip(), transforms.ToTensor(), transforms.Normalize((0.4914,0.4822,0.4465),(0.2023,0.1994,0.2010))])
    val_tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.4914,0.4822,0.4465),(0.2023,0.1994,0.2010))])
    return DataLoader(datasets.CIFAR10(data_dir, train=True, download=True, transform=train_tf), batch_size=batch_size, shuffle=True, num_workers=4), \
           DataLoader(datasets.CIFAR10(data_dir, train=False, download=False, transform=val_tf), batch_size=batch_size, shuffle=False, num_workers=4)

def train_epoch(model, loader, criterion, optimizer, device):
    model.train(); total_loss=0; correct=0; total=0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad(); out = model(imgs); loss = criterion(out, labels); loss.backward(); optimizer.step()
        total_loss += loss.item()*len(labels); correct += (out.argmax(1)==labels).sum().item(); total += len(labels)
    return total_loss/total, correct/total

def val_epoch(model, loader, criterion, device):
    model.eval(); total_loss=0; correct=0; total=0
    with torch.no_grad():
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            out = model(imgs); loss = criterion(out, labels)
            total_loss += loss.item()*len(labels); correct += (out.argmax(1)==labels).sum().item(); total += len(labels)
    return total_loss/total, correct/total

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=50); parser.add_argument('--batch_size', type=int, default=128)
    parser.add_argument('--lr', type=float, default=0.01); parser.add_argument('--data_dir', type=str, default='./data')
    parser.add_argument('--output_dir', type=str, default='./results'); parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args(); os.makedirs(args.output_dir, exist_ok=True)
    torch.manual_seed(args.seed); np.random.seed(args.seed)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}. CUDA: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'}")
    model = SimpleCNN().to(device); criterion = nn.CrossEntropyLoss(); optimizer = optim.Adam(model.parameters(), lr=args.lr)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    train_loader, val_loader = get_loaders(args.data_dir, args.batch_size)
    csv_path = os.path.join(args.output_dir, 'metrics.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f); writer.writerow(['epoch','train_loss','train_acc','val_loss','val_acc'])
        best_acc = 0
        for epoch in range(1, args.epochs+1):
            t0 = time.time(); tl, ta = train_epoch(model, train_loader, criterion, optimizer, device)
            vl, va = val_epoch(model, val_loader, criterion, device); scheduler.step()
            sec = time.time()-t0
            writer.writerow([epoch, f"{tl:.4f}", f"{ta:.4f}", f"{vl:.4f}", f"{va:.4f}"]); f.flush()
            if va > best_acc: best_acc = va; torch.save(model.state_dict(), os.path.join(args.output_dir, 'best_model.pth'))
            print(f"Epoch {epoch:3d}/{args.epochs} | {sec:5.1f}s | train_loss={tl:.4f} train_acc={ta:.4f} | val_loss={vl:.4f} val_acc={va:.4f} | best_acc={best_acc:.4f}")
        with open(os.path.join(args.output_dir, 'summary.json'), 'w') as sf:
            json.dump({'best_val_acc': best_acc, 'epochs': args.epochs, 'lr': args.lr, 'device': str(device)}, sf)  # import json
        print(f"Done. Best val_acc={best_acc:.4f}. Summary -> {args.output_dir}/summary.json")

if __name__ == '__main__':
    main()
