#include <bits/stdc++.h>
using namespace std;

int n, Q;
vector<vector<int>> dist;
vector<int> visited;
vector<int> x;
int load;
int f = 0;
int f_best = INT_MAX;
int c_min = INT_MAX;

bool check(int k, int v) {
    if(visited[v]) return false;
    if(v > n && !visited[v - n]) return false;
    if(v <= n && load + 1 > Q) return false;
    return true;
}

void Try(int k) {
    if(k > 2 * n) return;
    if(f + c_min * (2 * n - k + 1) >= f_best) return;

    for(int v = 1; v <= 2 * n; ++v) {
        if(!check(k, v)) continue;
        visited[v] = 1;
        x[k] = v;
        if(v <= n) ++load;
        else --load;
        f += dist[x[k - 1]][x[k]];

        if(k == 2 * n) {
            f_best = min(f_best, f + dist[x[k]][x[0]]);
        } else {
            Try(k + 1);
        }

        visited[v] = 0;
        if(v <= n) --load;
        else ++load;
        f -= dist[x[k - 1]][x[k]];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    cin >> n >> Q;

    dist.resize(2 * n + 1, vector<int>(2 * n + 1));
    x.resize(2 * n + 1);
    visited.assign(2 * n + 1, 0);
    visited[0] = 1;
    x[0] = 0;

    for(int i = 0; i <= 2 * n; ++i) {
        for(int j = 0; j <= 2 * n; ++j) {
            cin >> dist[i][j];
            if(i != j) c_min = min(c_min, dist[i][j]); 
        }
    }

    Try(1);
    cout << f_best << endl;
}