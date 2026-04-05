/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/26 18:00:21 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/03 16:40:37 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*ptr;
	size_t	i;
	size_t	l_s;

	if (!s)
		return (NULL);
	l_s = ft_strlen(s);
	if (start >= l_s)
		return (ft_strdup(""));
	if (len > l_s - start)
		len = l_s - start;
	ptr = malloc((len + 1) * sizeof(char));
	if (!ptr)
		return (NULL);
	i = 0;
	while (len > i)
	{
		*(ptr + i) = s[start + i];
		i++;
	}
	ptr[i] = '\0';
	return (ptr);
}
