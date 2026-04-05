/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/26 17:59:22 by tsellak           #+#    #+#             */
/*   Updated: 2025/10/26 17:59:46 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	count_words(char const *s, char c)
{
	int	count;
	int	is;

	count = 0;
	is = 0;
	while (*s)
	{
		if (*s != c && !is)
		{
			is = 1;
			count++;
		}
		else if (*s == c)
			is = 0;
		s++;
	}
	return (count);
}

static void	free_all(char **arr, int count)
{
	int	i;

	i = 0;
	while (i < count)
	{
		free(arr[i]);
		i++;
	}
	free(arr);
}

static char	**fill_word(const char *s, char c, char **result)
{
	int	i;
	int	j;
	int	start;

	i = 0;
	j = 0;
	start = -1;
	while (i <= (int)ft_strlen(s))
	{
		if (s[i] != c && start < 0)
			start = i;
		else if ((s[i] == c || i == (int)ft_strlen(s)) && start >= 0)
		{
			result[j] = ft_substr(s, start, i - start);
			if (!result[j])
				return (free_all(result, j), NULL);
			start = -1;
			j++;
		}
		i++;
	}
	result[j] = NULL;
	return (result);
}

char	**ft_split(char const *s, char c)
{
	char	**result;

	if (!s)
		return (NULL);
	result = malloc((count_words(s, c) + 1) * sizeof(char *));
	if (!result)
		return (NULL);
	return (fill_word(s, c, result));
}
